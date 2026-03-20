document.addEventListener('DOMContentLoaded', async () => {
  const apiDot = document.getElementById('apiDot');
  const apiText = document.getElementById('apiText');
  const platformStatus = document.getElementById('platformStatus');
  const problemStatus = document.getElementById('problemStatus');
  const openPanelBtn = document.getElementById('openPanelBtn');
  const settingsBtn = document.getElementById('settingsBtn');

  // Check API key
  chrome.runtime.sendMessage({ type: 'CHECK_API_KEY' }, (response) => {
    if (response?.hasKey) {
      apiDot.className = 'status-dot dot-green';
      apiText.textContent = 'Connected';
    } else {
      apiDot.className = 'status-dot dot-red';
      apiText.textContent = 'Not set';
    }
  });

  // Detect platform on active tab
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.id) {
      chrome.tabs.sendMessage(tab.id, { type: 'DETECT_PROBLEM' }, (response) => {
        if (chrome.runtime.lastError || !response) {
          platformStatus.textContent = 'Not a coding page';
          problemStatus.textContent = '-';
          return;
        }
        platformStatus.textContent = response.platform || 'Unknown';
        problemStatus.textContent = response.title || '-';
        problemStatus.title = response.title || '';
        openPanelBtn.disabled = false;
      });
    }
  } catch (e) {
    platformStatus.textContent = 'Not available';
  }

  openPanelBtn.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.id) {
      chrome.sidePanel.open({ tabId: tab.id });
      window.close();
    }
  });

  settingsBtn.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
});
