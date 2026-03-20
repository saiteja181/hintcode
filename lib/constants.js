const PLATFORMS = {
  LEETCODE: {
    name: 'LeetCode',
    hostname: 'leetcode.com',
    urlPattern: /leetcode\.com\/problems\//,
    color: '#FFA116',
  },
  HACKERRANK: {
    name: 'HackerRank',
    hostname: 'www.hackerrank.com',
    urlPattern: /hackerrank\.com\/challenges\/.*\/problem/,
    color: '#00EA64',
  },
  CODEFORCES: {
    name: 'CodeForces',
    hostname: 'codeforces.com',
    urlPattern: /codeforces\.com\/(problemset|contest)\/.*problem/,
    color: '#1890FF',
  },
  CODECHEF: {
    name: 'CodeChef',
    hostname: 'www.codechef.com',
    urlPattern: /codechef\.com\/problems\//,
    color: '#5B4638',
  },
  GEEKSFORGEEKS: {
    name: 'GeeksforGeeks',
    hostname: 'www.geeksforgeeks.org',
    urlPattern: /geeksforgeeks\.org\/problems\//,
    color: '#2F8D46',
  },
};

const AI_PROVIDERS = {
  groq: {
    name: 'Groq (Free, no card needed)',
    baseUrl: 'https://api.groq.com/openai/v1',
    defaultModel: 'llama-3.3-70b-versatile',
    models: ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'gemma2-9b-it', 'mixtral-8x7b-32768'],
    keyUrl: 'https://console.groq.com/keys',
    keyPlaceholder: 'gsk_...',
  },
  grok: {
    name: 'Grok / xAI (requires billing)',
    baseUrl: 'https://api.x.ai/v1',
    defaultModel: 'grok-3-mini',
    models: ['grok-3-mini', 'grok-3-mini-fast', 'grok-2-1212'],
    keyUrl: 'https://console.x.ai/',
    keyPlaceholder: 'xai-...',
  },
};

const DEFAULT_PROVIDER = 'groq';

const HINT_LEVELS = {
  NUDGE: 1,
  APPROACH: 2,
  DETAILED: 3,
  SOLUTION: 4,
};

const STORAGE_KEYS = {
  API_KEY: 'apiKey',
  PROVIDER: 'aiProvider',
  MODEL: 'aiModel',
  HINT_LANGUAGE: 'hintLanguage',
  HINT_CACHE: 'hintCache',
};

const DEFAULT_SETTINGS = {
  provider: DEFAULT_PROVIDER,
  model: AI_PROVIDERS[DEFAULT_PROVIDER].defaultModel,
  hintLanguage: 'english',
};
