# Using Playwright

This repository includes a Playwright-based scraper as an alternative to the
original Requests/BeautifulSoup implementation. Below is a short overview of the
benefits and potential drawbacks of using Playwright.

## Benefits

- **Handles dynamic pages**: Playwright can render JavaScript-driven pages,
  enabling scraping of sites that rely heavily on client-side scripts.
- **Cross-browser support**: Tests can run against Chromium, Firefox, or WebKit
  with a single API.
- **Powerful automation features**: Playwright offers robust capabilities for
  navigation, element interaction and waiting for network events.

## Drawbacks

- **Heavier dependencies**: Playwright requires downloading browser binaries,
  increasing setup time and disk usage.
- **Slower startup**: Launching a browser instance introduces overhead compared
  to plain HTTP requests.
- **More complex testing**: Unit tests must manage browser contexts which can
  slow down test execution.
