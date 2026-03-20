# Chrome Web Store Listing — HintCode

## Extension Name
HintCode — Coding Hints for Students

## Short Description (132 chars max)
Get progressive hints (not solutions) when stuck on LeetCode, HackerRank, CodeForces, CodeChef & GFG. Powered by Grok AI. Free.

## Detailed Description

Stuck on a coding problem? Don't look up the answer — get a hint instead.

HintCode (Smart Coding Hints for Students) is a Chrome extension that gives you progressive hints when you're stuck on coding problems. Instead of spoiling the solution, it guides your thinking step by step.

HOW IT WORKS

1. Navigate to a coding problem on any supported platform
2. Click the "Stuck? Get a Hint" button that appears on the page
3. Get a gentle nudge (Hint 1) — a subtle observation to shift your thinking
4. Still stuck? Get an approach hint (Hint 2) — names the technique you need
5. Need more? Get a detailed guide (Hint 3) — step-by-step in plain English
6. Last resort: Reveal the full solution with explanation

THREE LEVELS OF HINTS

- Hint 1 (Gentle Nudge): Makes one observation about the problem. Asks a guiding question. No algorithm names, no code.
- Hint 2 (Approach): Names the technique or data structure. Makes a concrete connection to the problem.
- Hint 3 (Detailed Guide): Step-by-step approach in plain English. Points out where your code diverges. Mentions edge cases. Still no code given.

SUPPORTED PLATFORMS

- LeetCode
- HackerRank
- CodeForces
- CodeChef
- GeeksforGeeks

FEATURES

- Auto-detects the problem statement and your code from the page
- Side panel UI stays open while you code
- Manual mode when auto-detection doesn't work
- Hint caching — navigate away and back without losing hints
- Works with your own free Grok API key (BYOK model)
- Dark theme that matches coding platforms

PRIVACY FIRST

- No data collection, no analytics, no telemetry
- Your code is sent only to Grok API using YOUR OWN API key
- No middleman server — direct browser-to-API communication
- API key stored in Chrome's encrypted sync storage
- Fully open source — audit every line

GETTING STARTED

1. Install the extension
2. Get your free Grok API key at console.x.ai
3. Click the extension icon → Settings → paste your key
4. Navigate to a coding problem and start learning!

Built for students, by developers who believe that struggling is where learning happens.

## Category
Education

## Language
English

## Privacy Practices (for Developer Dashboard)

### Single Purpose Description
This extension helps students learn coding by providing progressive AI-generated hints when they are stuck on coding problems on platforms like LeetCode, HackerRank, CodeForces, CodeChef, and GeeksforGeeks.

### Permission Justifications

| Permission | Justification |
|-----------|--------------|
| storage | Store user's API key, preferences, and cached hints locally |
| activeTab | Read the current coding problem and user's code from the active tab |
| sidePanel | Display the hint panel alongside the coding problem |
| host_permissions (coding sites) | Inject content scripts to detect problems and extract code on supported coding platforms |
| host_permissions (api.x.ai) | Make API calls to Grok AI to generate hints using the user's own API key |

### Data Usage Disclosure

| Data Type | Collected? | Usage |
|----------|-----------|-------|
| Personally identifiable info | No | - |
| Health info | No | - |
| Financial info | No | - |
| Authentication info | No | - |
| Personal communications | No | - |
| Location | No | - |
| Web history | No | - |
| User activity | No | - |
| Website content | Yes* | Problem statement and user code are read locally and sent to Grok API (user's own key) to generate hints. Never stored on any server. |

*Website content is processed locally and sent directly to a third-party API (xAI Grok) using the user's own API key. No data passes through our servers.

## Store Assets Checklist

- [ ] Extension icon: 128x128 PNG (icons/icon128.png)
- [ ] Small promo tile: 440x280 PNG (store-assets/promo-small-440x280.png)
- [ ] Large promo tile: 920x680 PNG (store-assets/promo-large-920x680.png)
- [ ] Screenshot 1: 1280x800 PNG (store-assets/screenshot-1-1280x800.png)
- [ ] Screenshot 2: 1280x800 PNG (store-assets/screenshot-2-1280x800.png)
- [ ] Screenshot 3: 1280x800 PNG (store-assets/screenshot-3-1280x800.png)

## Publishing Steps

1. Go to https://chrome.google.com/webstore/devconsole
2. Pay one-time $5 developer registration fee (if not already registered)
3. Click "New Item" -> upload the ZIP file (hintcode.zip)
4. Fill in listing details from this document
5. Upload promotional images and screenshots from store-assets/
6. Fill in Privacy Practices as documented above
7. Submit for review (typically 1-3 business days)
