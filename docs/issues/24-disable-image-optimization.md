# Issue 24: Disable Image Optimization for Text-to-Image

## Description

The images generated from text are currently being compressed, which can sometimes affect the clarity and sharpness of the text. Since these images are synthetically generated and should have a small file size to begin with, the compression step is unnecessary and should be removed to ensure maximum quality.

## Acceptance Criteria

- In the `generate_image_from_text` function, the call to `compress_image(image_path)` must be removed.
- The `compress_image` function itself should remain, as it is still used for other images (e.g., attachments), but it should not be called for images generated from text.
