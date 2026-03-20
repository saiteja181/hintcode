const GeeksforGeeks = {
  detect() {
    return (window.location.hostname.includes('geeksforgeeks.org')) &&
      window.location.pathname.includes('/problems/');
  },

  getProblemTitle() {
    const selectors = [
      '.problems_header_content__title h3',
      '.problems_header_content h3',
      'h3.problem-tab__title',
      '.problem-statement h2',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    const match = window.location.pathname.match(/\/problems\/([^/]+)/);
    if (match) return match[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return null;
  },

  getProblemStatement() {
    const selectors = [
      '.problems_header_content__description',
      '.problem-statement',
      '.problem_content',
      'div[class*="problemBody"]',
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
    return null;
  },

  getLanguage() {
    const selectors = [
      'button.languageSelected',
      '.lang-dropdown .selected',
      'select[class*="language"] option:checked',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },

  getDifficulty() {
    const selectors = [
      '.problems_header_content__difficulty',
      'span[class*="difficulty"]',
      '.difficulty',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },
};
