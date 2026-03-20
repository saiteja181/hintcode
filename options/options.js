const PROVIDERS = {
  groq: {
    name: 'Groq (Free, no card needed)',
    models: [
      { value: 'llama-3.3-70b-versatile', label: 'llama-3.3-70b-versatile (recommended)' },
      { value: 'llama-3.1-8b-instant', label: 'llama-3.1-8b-instant (fast)' },
      { value: 'gemma2-9b-it', label: 'gemma2-9b-it' },
      { value: 'mixtral-8x7b-32768', label: 'mixtral-8x7b-32768' },
    ],
    keyUrl: 'https://console.groq.com/keys',
    keyLabel: 'console.groq.com/keys',
    placeholder: 'gsk_...',
  },
  grok: {
    name: 'Grok / xAI (requires billing)',
    models: [
      { value: 'grok-3-mini', label: 'grok-3-mini' },
      { value: 'grok-3-mini-fast', label: 'grok-3-mini-fast' },
      { value: 'grok-2-1212', label: 'grok-2-1212' },
    ],
    keyUrl: 'https://console.x.ai/',
    keyLabel: 'console.x.ai',
    placeholder: 'xai-...',
  },
};

document.addEventListener('DOMContentLoaded', async () => {
  const providerSelect = document.getElementById('provider');
  const apiKeyInput = document.getElementById('apiKey');
  const toggleKeyBtn = document.getElementById('toggleKey');
  const saveKeyBtn = document.getElementById('saveKeyBtn');
  const testBtn = document.getElementById('testBtn');
  const keyStatus = document.getElementById('keyStatus');
  const keyLink = document.getElementById('keyLink');
  const modelSelect = document.getElementById('model');
  const hintLangSelect = document.getElementById('hintLanguage');
  const savePrefsBtn = document.getElementById('savePrefsBtn');
  const clearCacheBtn = document.getElementById('clearCacheBtn');
  const saveStatus = document.getElementById('saveStatus');

  // Load existing settings
  const data = await chrome.storage.sync.get(['apiKey', 'aiProvider', 'aiModel', 'hintLanguage']);
  const currentProvider = data.aiProvider || 'groq';

  providerSelect.value = currentProvider;
  updateProviderUI(currentProvider);

  if (data.apiKey) apiKeyInput.value = data.apiKey;
  if (data.aiModel) modelSelect.value = data.aiModel;
  if (data.hintLanguage) hintLangSelect.value = data.hintLanguage;

  // Provider change
  providerSelect.addEventListener('change', () => {
    const provider = providerSelect.value;
    updateProviderUI(provider);
    apiKeyInput.value = '';
    showStatus(keyStatus, '', '');
  });

  function updateProviderUI(provider) {
    const config = PROVIDERS[provider];
    apiKeyInput.placeholder = config.placeholder;
    keyLink.href = config.keyUrl;
    keyLink.textContent = config.keyLabel;

    // Update models dropdown
    modelSelect.innerHTML = '';
    config.models.forEach((m) => {
      const opt = document.createElement('option');
      opt.value = m.value;
      opt.textContent = m.label;
      modelSelect.appendChild(opt);
    });
  }

  // Toggle key visibility
  toggleKeyBtn.addEventListener('click', () => {
    const isPassword = apiKeyInput.type === 'password';
    apiKeyInput.type = isPassword ? 'text' : 'password';
    toggleKeyBtn.textContent = isPassword ? 'Hide' : 'Show';
  });

  // Save API key + provider
  saveKeyBtn.addEventListener('click', async () => {
    const key = apiKeyInput.value.trim();
    if (!key) {
      showStatus(keyStatus, 'Please enter an API key.', 'error');
      return;
    }
    await chrome.storage.sync.set({
      apiKey: key,
      aiProvider: providerSelect.value,
    });
    showStatus(keyStatus, 'API key saved!', 'success');
  });

  // Test connection
  testBtn.addEventListener('click', async () => {
    const key = apiKeyInput.value.trim();
    if (!key) {
      showStatus(keyStatus, 'Please enter an API key first.', 'error');
      return;
    }
    testBtn.disabled = true;
    testBtn.textContent = 'Testing...';
    showStatus(keyStatus, '', '');

    chrome.runtime.sendMessage(
      { type: 'TEST_CONNECTION', apiKey: key, provider: providerSelect.value },
      (response) => {
        testBtn.disabled = false;
        testBtn.textContent = 'Test Connection';
        if (response?.success) {
          showStatus(keyStatus, 'Connection successful! AI is ready.', 'success');
        } else {
          showStatus(keyStatus, response?.message || 'Connection failed.', 'error');
        }
      }
    );
  });

  // Save preferences
  savePrefsBtn.addEventListener('click', async () => {
    await chrome.storage.sync.set({
      aiModel: modelSelect.value,
      hintLanguage: hintLangSelect.value,
    });
    flashSaveStatus();
  });

  // Clear cache
  clearCacheBtn.addEventListener('click', async () => {
    const all = await chrome.storage.local.get(null);
    const hintKeys = Object.keys(all).filter((k) => k.startsWith('hint_'));
    if (hintKeys.length > 0) {
      await chrome.storage.local.remove(hintKeys);
    }
    clearCacheBtn.textContent = 'Cache cleared!';
    setTimeout(() => {
      clearCacheBtn.textContent = 'Clear Hint Cache';
    }, 2000);
  });

  function showStatus(el, message, type) {
    el.textContent = message;
    el.className = 'status' + (type ? ' ' + type : '');
  }

  function flashSaveStatus() {
    saveStatus.style.display = 'block';
    setTimeout(() => {
      saveStatus.style.display = 'none';
    }, 2000);
  }
});
