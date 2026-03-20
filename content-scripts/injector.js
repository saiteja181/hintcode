/* global PlatformDetector */

(function () {
  if (document.getElementById('hintcode-hint-btn')) return;

  // Wait a bit for page to fully load
  setTimeout(() => {
    const platform = PlatformDetector.detect();
    if (!platform) return;

    const btn = document.createElement('button');
    btn.id = 'hintcode-hint-btn';
    btn.textContent = 'Stuck? Get a Hint';
    btn.setAttribute('aria-label', 'Open HintCode hint panel');

    Object.assign(btn.style, {
      position: 'fixed',
      bottom: '24px',
      right: '24px',
      zIndex: '999999',
      padding: '12px 20px',
      background: 'linear-gradient(135deg, #7C3AED, #6D28D9)',
      color: '#ffffff',
      border: 'none',
      borderRadius: '50px',
      fontSize: '14px',
      fontWeight: '600',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      cursor: 'pointer',
      boxShadow: '0 4px 15px rgba(124, 58, 237, 0.4)',
      transition: 'all 0.3s ease',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    });

    // Lightbulb icon
    const icon = document.createElement('span');
    icon.textContent = '\u{1F4A1}';
    icon.style.fontSize = '16px';
    btn.prepend(icon);

    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'scale(1.05)';
      btn.style.boxShadow = '0 6px 20px rgba(124, 58, 237, 0.6)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = '0 4px 15px rgba(124, 58, 237, 0.4)';
    });

    btn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ type: 'OPEN_SIDE_PANEL' });
    });

    document.body.appendChild(btn);
  }, 1500);
})();
