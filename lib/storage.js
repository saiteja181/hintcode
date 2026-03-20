const Storage = {
  async getSync(keys) {
    return new Promise((resolve) => {
      chrome.storage.sync.get(keys, resolve);
    });
  },

  async setSync(data) {
    return new Promise((resolve) => {
      chrome.storage.sync.set(data, resolve);
    });
  },

  async getLocal(keys) {
    return new Promise((resolve) => {
      chrome.storage.local.get(keys, resolve);
    });
  },

  async setLocal(data) {
    return new Promise((resolve) => {
      chrome.storage.local.set(data, resolve);
    });
  },

  async removeLocal(keys) {
    return new Promise((resolve) => {
      chrome.storage.local.remove(keys, resolve);
    });
  },

  async getApiKey() {
    const data = await this.getSync([STORAGE_KEYS.API_KEY]);
    return data[STORAGE_KEYS.API_KEY] || null;
  },

  async setApiKey(key) {
    return this.setSync({ [STORAGE_KEYS.API_KEY]: key });
  },

  async getSettings() {
    const data = await this.getSync([
      STORAGE_KEYS.PROVIDER,
      STORAGE_KEYS.MODEL,
      STORAGE_KEYS.HINT_LANGUAGE,
    ]);
    const provider = data[STORAGE_KEYS.PROVIDER] || DEFAULT_SETTINGS.provider;
    return {
      provider: provider,
      model: data[STORAGE_KEYS.MODEL] || AI_PROVIDERS[provider].defaultModel,
      hintLanguage:
        data[STORAGE_KEYS.HINT_LANGUAGE] || DEFAULT_SETTINGS.hintLanguage,
    };
  },

  async setSettings(settings) {
    return this.setSync(settings);
  },

  _getCacheKey(url) {
    return `hint_${btoa(url).slice(0, 50)}`;
  },

  async getCachedHints(url) {
    const cacheKey = this._getCacheKey(url);
    const data = await this.getLocal([cacheKey]);
    return data[cacheKey] || null;
  },

  async setCachedHints(url, hints) {
    const cacheKey = this._getCacheKey(url);
    return this.setLocal({ [cacheKey]: hints });
  },

  async clearHintCache() {
    const all = await this.getLocal(null);
    const hintKeys = Object.keys(all).filter((k) => k.startsWith('hint_'));
    if (hintKeys.length > 0) {
      return this.removeLocal(hintKeys);
    }
  },
};
