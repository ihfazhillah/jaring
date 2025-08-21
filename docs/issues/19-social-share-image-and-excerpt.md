# Issue 19: Social Share Image and Excerpt Rendering

## Description

When sharing a link, the preview image and the excerpt are not always rendered correctly by social media platforms. This is likely due to missing or incorrect Open Graph meta tags in the HTML head of the message pages.

## Acceptance Criteria

- When a message page is shared on social media (e.g., Twitter, Facebook, Telegram), the preview should correctly display:
    - The main image of the post, if one exists (`og:image`).
    - The title of the post (`og:title`).
    - A concise summary or the beginning of the post content as the excerpt (`og:description`).
- The `og:image` tag should point to a full, absolute URL.
- The `og:description` should be plain text and properly truncated.
- The necessary Open Graph meta tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) must be present in the `<head>` section of the generated HTML for each message.
