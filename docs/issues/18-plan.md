
# Plan to Fix Incorrect Asset Output Path

The current implementation has issues with asset path generation when the output directory is not the root directory. This plan outlines the steps to fix this.

## Analysis

The core problem is that asset paths are either hardcoded or calculated based on a fixed directory structure, assuming the output directory is always the project's root.

The functions involved are:
- `generate_image_from_text`
- `copy_attachments`
- `main`

## Plan

### 1. Update `generate_image_from_text`

- **Action:** Modify the function to accept `output_path` as an argument.
- **Implementation:**
    - The function signature will be changed to `generate_image_from_text(text_content, post_id, image_index, author_name="Jaring", output_path)`.
    - The `image_path` will be constructed using `output_path`: `image_path = Path(output_path) / "assets/images" / image_filename`.
    - The returned path will be relative to the `output_path`, which is `f"assets/images/{image_filename}"`.

### 2. Update `copy_attachments`

- **Action:** Adjust the calculation of `new_relative_path` to be relative to the final HTML file's location.
- **Implementation:**
    - The `copy_attachments` function needs to be aware of the depth of the file it's processing relative to the `output_path`.
    - A new parameter `depth` will be added to `copy_attachments` to represent the nesting level of the output HTML file.
    - The `new_relative_path` will be calculated as `Path('../' * depth) / 'assets' / 'attachments' / image_source_path.name`.

### 3. Update `parse_file`

- **Action:** Pass the `output_path` and `depth` to the functions that need them.
- **Implementation:**
    - `parse_file` will be modified to accept a `depth` parameter.
    - `parse_file` will pass the `output_path` to `generate_image_from_text`.
    - `parse_file` will pass the `depth` to `copy_attachments`.

### 4. Update `main`

- **Action:** Pass the `depth` parameter when calling `parse_file`.
- **Implementation:**
    - When processing individual post pages, the `depth` will be `1` (`messages/`).
    - When processing the main `index.html`, the `depth` will be `0`.
    - The `depth` will also be passed to the templates for rendering.

This plan ensures that all asset paths are generated correctly, regardless of the configured output directory.
