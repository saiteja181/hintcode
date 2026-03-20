document.addEventListener('DOMContentLoaded', () => {
  // DOM elements
  const emptyState = document.getElementById('emptyState');
  const problemCard = document.getElementById('problemCard');
  const platformBadge = document.getElementById('platformBadge');
  const problemTitle = document.getElementById('problemTitle');
  const problemLang = document.getElementById('problemLang');
  const problemDiff = document.getElementById('problemDiff');
  const hintSection = document.getElementById('hintSection');
  const hintDisplay = document.getElementById('hintDisplay');
  const hint1Btn = document.getElementById('hint1Btn');
  const hint2Btn = document.getElementById('hint2Btn');
  const hint3Btn = document.getElementById('hint3Btn');
  const solutionBtn = document.getElementById('solutionBtn');
  const refreshBtn = document.getElementById('refreshBtn');
  const settingsBtn = document.getElementById('settingsBtn');
  const errorMsg = document.getElementById('errorMsg');
  const manualToggle = document.getElementById('manualToggle');
  const manualSection = document.getElementById('manualSection');
  const confirmOverlay = document.getElementById('confirmOverlay');
  const confirmCancel = document.getElementById('confirmCancel');
  const confirmYes = document.getElementById('confirmYes');

  let currentProblem = null;
  let hintsUsed = { 1: false, 2: false, 3: false };

  // Initialize
  detectProblem();

  // Event listeners
  refreshBtn.addEventListener('click', detectProblem);
  settingsBtn.addEventListener('click', () => chrome.runtime.openOptionsPage());
  hint1Btn.addEventListener('click', () => getHint(1));
  hint2Btn.addEventListener('click', () => getHint(2));
  hint3Btn.addEventListener('click', () => getHint(3));
  solutionBtn.addEventListener('click', () => {
    confirmOverlay.classList.add('active');
  });
  confirmCancel.addEventListener('click', () => {
    confirmOverlay.classList.remove('active');
  });
  confirmYes.addEventListener('click', () => {
    confirmOverlay.classList.remove('active');
    getSolution();
  });
  manualToggle.addEventListener('change', () => {
    manualSection.classList.toggle('active', manualToggle.checked);
    if (manualToggle.checked) {
      showHintSection();
    }
  });

  async function detectProblem() {
    hideError();
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab?.id) {
        showEmpty();
        return;
      }

      chrome.tabs.sendMessage(tab.id, { type: 'DETECT_PROBLEM' }, (response) => {
        if (chrome.runtime.lastError || !response) {
          showEmpty();
          return;
        }
        currentProblem = response;
        showProblem(response);
        loadCachedHints(response.url);
      });
    } catch (e) {
      showEmpty();
    }
  }

  function showProblem(data) {
    emptyState.style.display = 'none';
    problemCard.style.display = 'block';
    hintSection.style.display = 'block';
    platformBadge.textContent = data.platform;
    problemTitle.textContent = data.title;
    problemLang.textContent = data.language || 'Unknown';
    if (data.difficulty) {
      problemDiff.textContent = data.difficulty;
      problemDiff.style.display = '';
    } else {
      problemDiff.style.display = 'none';
    }
  }

  function showEmpty() {
    emptyState.style.display = 'block';
    problemCard.style.display = 'none';
    hintSection.style.display = 'none';
  }

  function showHintSection() {
    hintSection.style.display = 'block';
  }

  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.style.display = 'block';
  }

  function hideError() {
    errorMsg.style.display = 'none';
  }

  function getProblemData() {
    if (manualToggle.checked) {
      return {
        title: document.getElementById('manualTitle').value || 'Manual Problem',
        statement: document.getElementById('manualStatement').value || '',
        code: document.getElementById('manualCode').value || '',
        language: document.getElementById('manualLang').value,
        url: 'manual_' + document.getElementById('manualTitle').value,
        platform: 'Manual',
      };
    }
    return currentProblem;
  }

  async function getHint(level) {
    hideError();
    const problem = getProblemData();
    if (!problem && !manualToggle.checked) {
      showError('No problem detected. Try refreshing or use manual mode.');
      return;
    }

    const btn = [null, hint1Btn, hint2Btn, hint3Btn][level];
    const origHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Thinking...';

    chrome.runtime.sendMessage(
      {
        type: 'GET_HINT',
        level: level,
        title: problem.title,
        statement: problem.statement,
        code: problem.code,
        language: problem.language,
        url: problem.url,
      },
      (response) => {
        btn.innerHTML = origHTML;
        btn.disabled = false;

        if (response?.error) {
          showError(response.error);
          return;
        }

        if (response?.hint) {
          displayHint(level, response.hint);
          hintsUsed[level] = true;
          unlockNextHint(level);
        }
      }
    );
  }

  async function getSolution() {
    hideError();
    const problem = getProblemData();
    if (!problem && !manualToggle.checked) {
      showError('No problem detected.');
      return;
    }

    const origText = solutionBtn.textContent;
    solutionBtn.disabled = true;
    solutionBtn.innerHTML = '<span class="spinner"></span> Generating solution...';

    chrome.runtime.sendMessage(
      {
        type: 'GET_SOLUTION',
        title: problem.title,
        statement: problem.statement,
        code: problem.code,
        language: problem.language,
        url: problem.url,
      },
      (response) => {
        solutionBtn.textContent = origText;
        solutionBtn.disabled = false;

        if (response?.error) {
          showError(response.error);
          return;
        }

        if (response?.solution) {
          displaySolution(response.solution);
        }
      }
    );
  }

  function displayHint(level, text) {
    // Remove existing hint card for this level if any
    const existingId = `hintCard${level}`;
    const existing = document.getElementById(existingId);
    if (existing) existing.remove();

    const labels = { 1: 'Hint 1 - Gentle Nudge', 2: 'Hint 2 - Approach', 3: 'Hint 3 - Detailed Guide' };
    const card = document.createElement('div');
    card.id = existingId;
    card.className = `hint-card hint-card-${level}`;
    card.innerHTML = `<div class="hint-label">${labels[level]}</div>${escapeHtml(text)}`;

    hintDisplay.appendChild(card);
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function displaySolution(text) {
    const existingId = 'solutionCard';
    const existing = document.getElementById(existingId);
    if (existing) existing.remove();

    const card = document.createElement('div');
    card.id = existingId;
    card.className = 'hint-card hint-card-solution';
    card.innerHTML = `<div class="hint-label">Full Solution</div>${escapeHtml(text)}`;

    hintDisplay.appendChild(card);
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function unlockNextHint(currentLevel) {
    if (currentLevel === 1) hint2Btn.disabled = false;
    if (currentLevel === 2) hint3Btn.disabled = false;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  async function loadCachedHints(url) {
    const data = await chrome.storage.local.get(null);
    const cacheKey = `hint_${btoa(url).slice(0, 50)}`;
    const cached = data[cacheKey];
    if (!cached) return;

    if (cached.hint1) {
      displayHint(1, cached.hint1);
      hintsUsed[1] = true;
      hint2Btn.disabled = false;
    }
    if (cached.hint2) {
      displayHint(2, cached.hint2);
      hintsUsed[2] = true;
      hint3Btn.disabled = false;
    }
    if (cached.hint3) {
      displayHint(3, cached.hint3);
      hintsUsed[3] = true;
    }
    if (cached.solution) {
      displaySolution(cached.solution);
    }
  }
});
