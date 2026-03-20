/* global LeetCode, HackerRank, CodeForces, CodeChef, GeeksforGeeks, PLATFORMS */

function normalizeLanguage(raw) {
  if (!raw) return 'Unknown';
  const lang = raw.toLowerCase().trim();
  const map = {
    'c++': 'C++', 'cpp': 'C++', 'c++14': 'C++', 'c++17': 'C++', 'c++20': 'C++',
    'python': 'Python', 'python3': 'Python', 'python2': 'Python', 'pypy': 'Python', 'pypy3': 'Python',
    'java': 'Java', 'java 8': 'Java', 'java 11': 'Java', 'java 17': 'Java',
    'javascript': 'JavaScript', 'js': 'JavaScript', 'node': 'JavaScript', 'nodejs': 'JavaScript',
    'typescript': 'TypeScript', 'ts': 'TypeScript',
    'c': 'C', 'c11': 'C',
    'go': 'Go', 'golang': 'Go',
    'rust': 'Rust',
    'ruby': 'Ruby',
    'swift': 'Swift',
    'kotlin': 'Kotlin',
    'scala': 'Scala',
    'php': 'PHP',
    'c#': 'C#', 'csharp': 'C#',
    'dart': 'Dart',
    'r': 'R',
    'sql': 'SQL', 'mysql': 'SQL',
  };
  for (const [key, value] of Object.entries(map)) {
    if (lang.includes(key)) return value;
  }
  return raw.trim();
}

const PlatformDetector = {
  _platforms: [
    { key: 'LEETCODE', module: typeof LeetCode !== 'undefined' ? LeetCode : null },
    { key: 'HACKERRANK', module: typeof HackerRank !== 'undefined' ? HackerRank : null },
    { key: 'CODEFORCES', module: typeof CodeForces !== 'undefined' ? CodeForces : null },
    { key: 'CODECHEF', module: typeof CodeChef !== 'undefined' ? CodeChef : null },
    { key: 'GEEKSFORGEEKS', module: typeof GeeksforGeeks !== 'undefined' ? GeeksforGeeks : null },
  ],

  detect() {
    for (const platform of this._platforms) {
      if (platform.module && platform.module.detect()) {
        return {
          key: platform.key,
          module: platform.module,
          info: typeof PLATFORMS !== 'undefined' ? PLATFORMS[platform.key] : { name: platform.key },
        };
      }
    }
    return null;
  },

  extractProblemData() {
    const platform = this.detect();
    if (!platform) return null;

    const mod = platform.module;
    return {
      platform: platform.info.name || platform.key,
      platformKey: platform.key,
      url: window.location.href,
      title: mod.getProblemTitle() || 'Unknown Problem',
      statement: mod.getProblemStatement() || '',
      code: mod.getUserCode() || '',
      language: normalizeLanguage(mod.getLanguage()),
      difficulty: (mod.getDifficulty && mod.getDifficulty()) || null,
    };
  },
};

// Listen for messages from sidepanel/popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'DETECT_PROBLEM') {
    const data = PlatformDetector.extractProblemData();
    sendResponse(data);
  }
  return true;
});
