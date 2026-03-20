const AIClient = {
  async callChat(messages, apiKey, provider, model) {
    const providerConfig = AI_PROVIDERS[provider] || AI_PROVIDERS[DEFAULT_PROVIDER];
    const selectedModel = model || providerConfig.defaultModel;
    const url = `${providerConfig.baseUrl}/chat/completions`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: selectedModel,
        messages: messages,
        temperature: 0.7,
        max_tokens: 1024,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const apiMsg = errorData.error?.message || '';
      if (response.status === 401) {
        throw new Error('Invalid API key. Please check your API key in settings.');
      }
      if (response.status === 403) {
        throw new Error(
          'Access denied (403). Your account may not have API access enabled. Check your billing/credits at the provider dashboard.'
        );
      }
      if (response.status === 429) {
        throw new Error('Rate limit exceeded. Please wait a moment and try again.');
      }
      if (response.status === 400) {
        throw new Error(
          `Bad request (model: ${selectedModel}): ${apiMsg || 'Try a different model in Settings.'}`
        );
      }
      throw new Error(apiMsg || `API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
  },

  async testConnection(apiKey, provider) {
    try {
      const result = await this.callChat(
        [{ role: 'user', content: 'Say "connected" in one word.' }],
        apiKey,
        provider
      );
      return { success: true, message: result };
    } catch (error) {
      return { success: false, message: error.message };
    }
  },
};
