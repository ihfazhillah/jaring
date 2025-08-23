# Issue 26: No-JavaScript Pagination

## Description

The current pagination system relies on JavaScript to fetch and load subsequent pages, which means it does not work for users who have JavaScript disabled. A fallback mechanism is needed to ensure that all users can navigate through all the posts.

## Acceptance Criteria

- The system should generate traditional pagination links (e.g., "Previous", "1", "2", "3", "Next") in the HTML.
- These links should point to static HTML pages (e.g., `index.html`, `page-2.html`, `page-3.html`).
- The JavaScript-based infinite scroll/lazy loading should be layered on top of this static pagination.
- If JavaScript is disabled, the static links will be visible and functional.
- If JavaScript is enabled, the script can optionally hide the static links and take over the pagination, providing the infinite scroll experience.
- This will require changes to the `main` function to generate the necessary static pages and to the `index.html` and `tag_index.html` templates to include the static pagination links.
