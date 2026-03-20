const LeetCode = {
  detect() {
    return window.location.hostname === 'leetcode.com' &&
      window.location.pathname.includes('/problems/');
  },

  getProblemTitle() {
    const selectors = [
      '[data-cy="question-title"]',
      '.text-title-large a',
      '.text-title-large',
      'div[class*="title"] a',
      'h4[data-cy="question-title"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    // Fallback: extract from URL
    const match = window.location.pathname.match(/\/problems\/([^/]+)/);
    if (match) return match[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return null;
  },

  getProblemStatement() {
    const selectors = [
      '[data-track-load="description_content"]',
      '.elfjS',
      'div[class*="description"]',
      '.question-content',
      'div[data-key="description-content"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim().slice(0, 3000);
    }
    return null;
  },

  getUserCode() {
    // Monaco editor
    const monacoLines = document.querySelectorAll('.view-lines .view-line');
    if (monacoLines.length > 0) {
      return Array.from(monacoLines).map(l => l.textContent).join('\n');
    }
    // CodeMirror fallback
    const cm = document.querySelector('.CodeMirror');
    if (cm?.CodeMirror) return cm.CodeMirror.getValue();
    return null;
  },

  getLanguage() {
    const selectors = [
      'button[id*="lang"]',
      'div[class*="lang-select"] button',
      '[class*="ant-select-selection-item"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },

  getDifficulty() {
    const selectors = [
      'div[class*="difficulty"]',
      'span[class*="difficulty"]',
      'div[diff]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) {
        const text = el.textContent.trim().toLowerCase();
        if (text.includes('easy')) return 'Easy';
        if (text.includes('medium')) return 'Medium';
        if (text.includes('hard')) return 'Hard';
      }
    }
    return null;
  },
};
