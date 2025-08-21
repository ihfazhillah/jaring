# Issue 21: RTL, LTR, and Mixed-Direction Text Handling

## Description

The system currently does not explicitly handle text with different writing directions, such as Right-to-Left (RTL) for Arabic and Left-to-Right (LTR) for Indonesian. When a file contains mixed-direction text (e.g., a line of Arabic followed by a line of Indonesian), it may not render correctly in the final HTML output or in the generated images.

## Acceptance Criteria

### In HTML Output:
- There should be a mechanism to specify the primary direction of a post (e.g., via frontmatter: `direction: rtl`).
- The `<html>` tag should have the appropriate `dir` attribute (`dir="rtl"` or `dir="ltr"`).
- For mixed content, there should be a way to wrap text blocks in elements with the correct `dir` attribute to ensure they are displayed correctly. This could be an automatic detection or a manual markdown extension.

### In Generated Images:
- The `pictex` image generation logic needs to be updated to handle RTL text.
- The library used for rendering text in images must support RTL shaping (e.g., properly connecting Arabic letters).
- When a line is identified as RTL (e.g., Arabic), it should be rendered with the correct alignment and direction within the image.
- When a line is LTR, it should be rendered as it is currently.
