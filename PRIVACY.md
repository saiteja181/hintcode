# Privacy Policy

HintCode is designed with privacy as a core principle.

## What We Collect

**Nothing.** HintCode does not collect, store, or transmit any user data to our servers. We have no servers.

## How Your Data Flows

1. The extension reads the problem statement and your code **locally** from the webpage DOM
2. This data is sent **directly** from the extension's service worker to the Grok API (`api.x.ai`) using **your own API key**
3. The response is displayed in the side panel and cached **locally** in your browser

That's it. No middleman, no analytics, no telemetry.

## Your API Key

- Stored in `chrome.storage.sync`, which is encrypted and tied to your Google account
- Never sent anywhere except to `api.x.ai` for API calls
- Never accessible to content scripts (only the background service worker)
- You can delete it at any time from the Settings page

## Third-Party Services

The only external service HintCode communicates with is:

- **xAI Grok API** (`api.x.ai`) — to generate hints and solutions

Your interactions with Grok are governed by [xAI's privacy policy](https://x.ai/legal/privacy-policy).

## Local Storage

HintCode stores the following data locally in your browser:
- Your API key (chrome.storage.sync)
- Your preferences (model, language — chrome.storage.sync)
- Cached hints for previously visited problems (chrome.storage.local)

All of this can be cleared from the Settings page or by removing the extension.

## Open Source

This extension is fully open source. You can audit every line of code to verify these claims.
