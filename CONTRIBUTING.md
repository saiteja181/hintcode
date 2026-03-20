# Contributing to HintCode

Thank you for your interest in contributing! This guide will help you get started.

## Quick Start

1. Fork the repo and clone it
2. Load the extension in Chrome (`chrome://extensions/` → Developer mode → Load unpacked)
3. Make your changes
4. Test on actual coding platform pages
5. Submit a pull request

## Adding a New Platform

This is the most common contribution. Each platform is a single file in `content-scripts/platforms/`.

### Steps:

1. Create `content-scripts/platforms/yourplatform.js`
2. Implement the platform object with these methods:

```javascript
const YourPlatform = {
  detect() {
    // Return true if current page is this platform's problem page
    return window.location.hostname.includes('yourplatform.com');
  },

  getProblemTitle() {
    // Return the problem title as a string, or null
  },

  getProblemStatement() {
    // Return the problem description text (max 3000 chars), or null
  },

  getUserCode() {
    // Return the user's code from the editor, or null
  },

  getLanguage() {
    // Return the selected programming language, or null
  },

  getDifficulty() {
    // Return difficulty level if available, or null
  },
};
```

3. Add the platform to `lib/constants.js` in the `PLATFORMS` object
4. Register it in `content-scripts/detector.js` in the `_platforms` array
5. Add URL patterns to `manifest.json` (content_scripts matches + host_permissions)
6. Test on real problem pages

### Tips for Writing Selectors

- Always provide **multiple fallback selectors** — platforms change their DOM frequently
- Use `data-*` attributes when available (more stable than class names)
- Test with at least 3 different problems
- Include a URL-based fallback for `getProblemTitle()`

## Code Style

- Vanilla JavaScript (no TypeScript, no JSX)
- No build step required for development
- Use `const`/`let`, never `var`
- Descriptive function and variable names
- Comments only where the logic isn't self-evident

## Pull Request Process

1. Create a feature branch from `main`
2. Make focused, single-purpose commits
3. Test your changes on real coding platform pages
4. Fill out the PR template
5. Wait for review

## Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:
- Which platform and problem URL
- What you expected vs. what happened
- Browser version
- Console errors (if any)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md).
