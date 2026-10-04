"use strict";
const $ = (id) => document.getElementById(id);
let requestSequence = 0;
const pad = (n) => String(n).padStart(2, "0");
const today = new Date();
$("day").value = `${today.getFullYear()}-${pad(today.getMonth() + 1)}-${pad(today.getDate())}`;
for (let minute = 540; minute <= 1080; minute += 30) {
  const time = `${pad(Math.floor(minute / 60))}:${pad(minute % 60)}`;
  if (minute < 1080) $("start").add(new Option(time, time));
  if (minute > 540) $("end").add(new Option(time, time));
}
$("start").value = "10:00";
$("end").value = "11:00";
function message(text, error = false) {
  $("message").textContent = text;
  $("message").className = error ? "message error" : "message";
}
async function api(path, options) {
  let response;
  try { response = await fetch(path, options); }
  catch (_) { throw new Error("连接失败，请确认本地服务仍在运行；恢复连接后刷新列表核对结果。"); }
  const body = await response.json();
  if (!response.ok) throw new Error(body.error?.message || "操作失败，请刷新后重试。");
  return body;
}
async function loadBookings(notice) {
  const sequence = ++requestSequence;
  const day = $("day").value;
  $("date-label").textContent = `${day || "请选择日期"} · 教学会议室`;
  $("bookings").replaceChildren();
  if (!day) { message("请先选择有效日期。", true); return; }
  message("正在读取当天预约…");
  try {
    const body = await api(`/api/bookings?date=${encodeURIComponent(day)}`);
    if (sequence !== requestSequence) return;
    for (const item of body.bookings) {
      const row = document.createElement("div"); row.className = "booking";
      const main = document.createElement("div"); main.className = "booking-main";
      const time = document.createElement("div"); time.className = "booking-time";
      time.textContent = `${item.start} — ${item.end}`;
      const detail = document.createElement("div"); detail.className = "booking-detail";
      detail.textContent = `${item.name} · ${item.purpose}`;
      const cancel = document.createElement("button"); cancel.className = "cancel"; cancel.type = "button";
      cancel.textContent = "取消预约";
      cancel.setAttribute("aria-label", `取消 ${item.start} 到 ${item.end} 的预约`);
      cancel.addEventListener("click", () => {
        cancel.hidden = true;
        const confirmation = document.createElement("div"); confirmation.className = "cancel-confirmation";
        confirmation.setAttribute("role", "group");
        confirmation.setAttribute("aria-label", `确认取消 ${item.date} ${item.start} 到 ${item.end} 的预约`);
        const prompt = document.createElement("p");
        prompt.textContent = `取消 ${item.date} ${item.start}—${item.end} 的预约？`;
        const confirm = document.createElement("button"); confirm.type = "button"; confirm.className = "cancel";
        confirm.textContent = "确认取消";
        const keep = document.createElement("button"); keep.type = "button"; keep.className = "subtle";
        keep.textContent = "保留预约";
        keep.addEventListener("click", () => { confirmation.remove(); cancel.hidden = false; cancel.focus(); });
        confirm.addEventListener("click", async () => {
          confirm.disabled = true; keep.disabled = true;
          try { await api(`/api/bookings/${item.id}`, { method: "DELETE" }); await loadBookings("已取消。该时段可以重新预约。"); }
          catch (error) { message(error.message, true); confirm.disabled = false; keep.disabled = false; }
        });
        confirmation.append(prompt, confirm, keep); row.append(confirmation); keep.focus();
      });
      main.append(time, detail); row.append(main, cancel); $("bookings").append(row);
    }
    if (!body.bookings.length) {
      const empty = document.createElement("p"); empty.className = "empty";
      empty.textContent = "当天还没有预约。试着建立第一条记录。"; $("bookings").append(empty);
    }
    message(notice || `已从数据库读取 ${body.bookings.length} 条预约。`);
  } catch (error) { if (sequence === requestSequence) message(error.message, true); }
}
$("booking-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.currentTarget));
  $("submit").disabled = true;
  try {
    await api("/api/bookings", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    await loadBookings("预约成功。现在可以刷新页面，检查记录是否保留。");
  } catch (error) { message(error.message, true); }
  finally { $("submit").disabled = false; }
});
$("day").addEventListener("change", () => loadBookings());
$("refresh").addEventListener("click", () => loadBookings());
loadBookings();
