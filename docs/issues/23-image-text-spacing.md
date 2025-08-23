# Issue 23: Adjust Text Spacing in Generated Images

## Description

The spacing between text elements in the images generated from text is not ideal. There should be more space between individual lines of content and a larger space between the main content and the author's name to improve visual hierarchy and readability.

## Acceptance Criteria

- In the `generate_image_from_text` function, the `pictex` layout needs to be adjusted.
- A gap of 2px should be added between each `Text()` object that represents a line of the main content.
- A larger gap of 4px should be added between the block of content text and the `Row` containing the author's name.
- This will likely involve modifying the `gap` property of the `Column` and `Row` elements in the `pictex` layout.
