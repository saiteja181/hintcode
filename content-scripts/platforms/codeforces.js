const CodeForces = {
  detect() {
    return window.location.hostname === 'codeforces.com' &&
      (window.location.pathname.includes('/problem/') ||
       window.location.pathname.includes('/problemset/problem/'));
  },

  getProblemTitle() {
    const selectors = [
      '.problem-statement .title',
      '#pageContent .title',
      '.header .title',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el?.textContent?.trim()) return el.textContent.trim();
    }
    return null;
  },

  getProblemStatement() {
    const el = document.querySelector('.problem-statement');
    if (el?.textContent?.trim()) return el.textContent.trim().slice(0, 3000);
    return null;
  },

  getUserCode() {
    // ACE editor
    const aceEditor = document.querySelector('.ace_editor');
    if (aceEditor?.env?.editor) return aceEditor.env.editor.getValue();
    // Textarea fallback
    const ta = document.querySelector('#sourceCodeTextarea, textarea[name="source"]');
    if (ta) return ta.value;
    return null;
  },

  getLanguage() {
    const sel = document.querySelector('select[name="programTypeId"] option:checked');
    if (sel?.textContent?.trim()) return sel.textContent.trim();
    return null;
  },

  getDifficulty() {
    const tags = document.querySelectorAll('.tag-box');
    for (const tag of tags) {
      const text = tag.textContent.trim();
      if (text.match(/^\*\d+$/)) return text;
    }
    return null;
  },
};
