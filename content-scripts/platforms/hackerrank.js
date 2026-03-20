const HackerRank = {
  detect() {
    return window.location.hostname.includes('hackerrank.com') &&
      window.location.pathname.includes('/challenges/');
  },

  getProblemTitle() {
    const selectors = [
      '.challenge-view h2',
      '.challengeTitle h2',
      '.challenge-name',
      'h2.ui-title',
      '.hr-challenge-name h2',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    const match = window.location.pathname.match(/\/challenges\/([^/]+)/);
    if (match) return match[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return null;
  },

  getProblemStatement() {
    const selectors = [
      '.challenge-body-html',
      '.problem-statement',
      '.challenge_problem_statement',
      '.challenge-text',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim().slice(0, 3000);
    }
    return null;
  },

  getUserCode() {
    // CodeMirror
    const cm = document.querySelector('.CodeMirror');
    if (cm?.CodeMirror) return cm.CodeMirror.getValue();
    // Monaco
    const monacoLines = document.querySelectorAll('.view-lines .view-line');
    if (monacoLines.length > 0) {
      return Array.from(monacoLines).map(l => l.textContent).join('\n');
    }
    // Textarea fallback
    const ta = document.querySelector('.custom-input textarea, #input textarea');
    if (ta) return ta.value;
    return null;
  },

  getLanguage() {
    const selectors = [
      '.select-language .is-selected',
      '#select-lang .select-selected',
      'select.select-language',
      '[class*="language-selector"] [class*="selected"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },

  getDifficulty() {
    const selectors = [
      '.difficulty-block span',
      '.sidebar-problem-difficulty',
      'span[class*="difficulty"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },
};
