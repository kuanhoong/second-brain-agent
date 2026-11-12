const $ = id => document.getElementById(id);
let tab = null, text = "";

(async () => {
  [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  $("page").textContent = tab.title || tab.url;
  try { text = await selectionOf(tab.id); } catch (e) { text = ""; }
  if (!text) { $("quote").textContent = "Highlight some text on the page first, then open this again."; return; }
  $("quote").textContent = text.length > 600 ? text.slice(0, 600) + "…" : text;
  $("save").disabled = false;
})();

$("save").onclick = async () => {
  $("save").disabled = true;
  $("status").textContent = "Saving the highlight…";
  try {
    const job = await sendHighlight(tab.url, tab.title, text);
    $("status").textContent = "Highlight saved. Gemini is summarising and tagging…";
    const done = await waitForJob(job.id);
    const out = $("status");
    out.textContent = "";
    if (done.state === "done") {
      out.append(`Filed as ${done.concept}. Linked to ${done.linked_to.length} concept(s). `);
      for (const t of done.tags) { const s = document.createElement("span"); s.className = "tag"; s.textContent = t; out.append(s); }
    } else {
      out.textContent = `Highlight kept in ${job.source}, but not summarised yet. ${done.error || ""}`;
    }
  } catch (err) {
    $("status").textContent = `Could not reach the second brain. Is graph_server.py running? (${err.message})`;
    $("save").disabled = false;
  }
};
