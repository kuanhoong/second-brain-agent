// Right-click menu and keyboard shortcut. The popup handles the toolbar button.
importScripts("shared.js");

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({ id: "capture-highlight", title: "Save highlight to Second Brain", contexts: ["selection"] });
});

async function badge(tabId, text, color) {
  await chrome.action.setBadgeBackgroundColor({ color, tabId });
  await chrome.action.setBadgeText({ text, tabId });
}

async function capture(tab, text) {
  if (!tab || !tab.id) return;
  try {
    text = (text || (await selectionOf(tab.id))).trim();
    if (!text) return badge(tab.id, "?", "#6B6880");
    await badge(tab.id, "…", "#F59E0B");
    const job = await sendHighlight(tab.url, tab.title, text);
    const done = await waitForJob(job.id);
    await badge(tab.id, done.state === "done" ? "✓" : "!", done.state === "done" ? "#10B981" : "#EC4899");
  } catch (err) {
    await badge(tab.id, "!", "#EC4899");
  }
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "capture-highlight") capture(tab, info.selectionText);
});
chrome.commands.onCommand.addListener((command, tab) => {
  if (command === "capture-highlight") capture(tab, "");
});
