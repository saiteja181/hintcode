const CodeChef = {
  detect() {
    return window.location.hostname.includes('codechef.com') &&
      window.location.pathname.includes('/problems/');
  },

  getProblemTitle() {
    const selectors = [
      'h1',
      '.problem-name',
      '.breadcrumbs span:last-child',
      'aside h3',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    const match = window.location.pathname.match(/\/problems\/([^/]+)/);
    if (match) return match[1];
    return null;
  },

  getProblemStatement() {
    const selectors = [
      '.problem-statement',
      '#problem-statement',
      '.problem-description',
      'div[class*="problemBody"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim().slice(0, 3000);
    }
    return null;
  },

  getUserCode() {
    // Monaco
    const monacoLines = document.querySelectorAll('.view-lines .view-line');
    if (monacoLines.length > 0) {
      return Array.from(monacoLines).map(l => l.textContent).join('\n');
    }
    return null;
  },

  getLanguage() {
    const selectors = [
      'button[class*="language"] span',
      'div[class*="language-selector"]',
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
      'span[class*="diff"]',
      '.difficulty-tag',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },
};
