// Shared by the popup and the service worker.
const SERVER = "http://127.0.0.1:8765";

async function sendHighlight(url, title, text) {
  const res = await fetch(`${SERVER}/api/capture`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, title, text }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error || `Server said ${res.status}`);
  return body;
}

async function waitForJob(id, onUpdate) {
  for (let i = 0; i < 90; i++) {
    const job = await (await fetch(`${SERVER}/api/capture?id=${id}`)).json();
    if (onUpdate) onUpdate(job);
    if (job.state !== "summarising") return job;
    await new Promise(r => setTimeout(r, 1000));
  }
  return { state: "timeout" };
}

async function selectionOf(tabId) {
  const [frame] = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => window.getSelection().toString(),
  });
  return (frame && frame.result ? frame.result : "").trim();
}
