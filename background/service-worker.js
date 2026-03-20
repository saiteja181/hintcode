importScripts(
  '/lib/constants.js',
  '/lib/storage.js',
  '/lib/grok-api.js',
  '/lib/prompts.js'
);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case 'GET_HINT':
      handleGetHint(message, sendResponse);
      return true;

    case 'GET_SOLUTION':
      handleGetSolution(message, sendResponse);
      return true;

    case 'CHECK_API_KEY':
      handleCheckApiKey(sendResponse);
      return true;

    case 'TEST_CONNECTION':
      handleTestConnection(message.apiKey, message.provider, sendResponse);
      return true;

    case 'OPEN_SIDE_PANEL':
      openSidePanel(sender.tab);
      return false;
  }
});

async function handleGetHint(message, sendResponse) {
  try {
    const apiKey = await Storage.getApiKey();
    if (!apiKey) {
      sendResponse({ error: 'No API key configured. Please add your API key in settings.' });
      return;
    }

    const settings = await Storage.getSettings();
    const { level, title, statement, code, language, url } = message;

    // Check cache first
    const cached = await Storage.getCachedHints(url);
    if (cached && cached[`hint${level}`]) {
      sendResponse({ hint: cached[`hint${level}`], cached: true });
      return;
    }

    const messages = Prompts.buildHintPrompt(level, title, statement, code, language);
    const hint = await AIClient.callChat(messages, apiKey, settings.provider, settings.model);

    // Cache the hint
    const existingCache = cached || {};
    existingCache[`hint${level}`] = hint;
    await Storage.setCachedHints(url, existingCache);

    sendResponse({ hint, cached: false });
  } catch (error) {
    sendResponse({ error: error.message });
  }
}

async function handleGetSolution(message, sendResponse) {
  try {
    const apiKey = await Storage.getApiKey();
    if (!apiKey) {
      sendResponse({ error: 'No API key configured. Please add your API key in settings.' });
      return;
    }

    const settings = await Storage.getSettings();
    const { title, statement, code, language, url } = message;

    const cached = await Storage.getCachedHints(url);
    if (cached && cached.solution) {
      sendResponse({ solution: cached.solution, cached: true });
      return;
    }

    const messages = Prompts.buildHintPrompt(
      HINT_LEVELS.SOLUTION, title, statement, code, language
    );
    const solution = await AIClient.callChat(messages, apiKey, settings.provider, settings.model);

    const existingCache = cached || {};
    existingCache.solution = solution;
    await Storage.setCachedHints(url, existingCache);

    sendResponse({ solution, cached: false });
  } catch (error) {
    sendResponse({ error: error.message });
  }
}

async function handleCheckApiKey(sendResponse) {
  const apiKey = await Storage.getApiKey();
  sendResponse({ hasKey: !!apiKey });
}

async function handleTestConnection(apiKey, provider, sendResponse) {
  const result = await AIClient.testConnection(apiKey, provider);
  sendResponse(result);
}

function openSidePanel(tab) {
  if (tab?.id) {
    chrome.sidePanel.open({ tabId: tab.id }).catch(() => {});
  }
}

chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: false }).catch(() => {});
