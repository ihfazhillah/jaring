# Issue 27: Pagination Fallback for Local Files

## Description

The JavaScript-based pagination fails when opening the generated HTML files directly from the local filesystem (i.e., using a `file:///` URL) because `fetch()` requests are subject to the browser's same-origin policy and are often blocked for local files. This results in a broken pagination experience even when JavaScript is enabled.

## Acceptance Criteria

- The JavaScript code for pagination needs to be updated to detect if the page is being viewed from the local filesystem.
- If the page is a local file, the script should not attempt to `fetch()` the subsequent pages.
- Instead, the script should ensure that the static HTML pagination links (implemented in Issue #26) remain visible and functional.
- This provides a graceful degradation of the user experience, falling back to the non-JavaScript version when the infinite scroll cannot be initiated.
