# Issue 20: Easy and Correct File Linking

## Description

There needs to be a simple and robust way to link between different posts within the project. This linking should be easy for the author to write and should be correctly resolved to the final HTML path during the site generation process.

Two primary methods of linking should be supported:
1.  **By ID:** Linking using the unique post ID (e.g., `1447-02-01-maafkan-lapang-dada`).
2.  **By Filename:** Linking using the relative path to the markdown file (e.g., `../nak/1447-02-01-maafkan-lapang-dada.md`).

## Acceptance Criteria

- A new custom syntax (e.g., `[[link-target]]`) should be introduced to handle these internal links.
- The system must be able to parse this syntax from the markdown content.
- During site generation, the `[[link-target]]` should be replaced with a valid HTML `<a>` tag pointing to the correct generated file.
- The link resolver must be able to find the target post by either its ID or its filename.
- If the link target cannot be found, the system should log a warning and, if possible, render the link in a way that indicates it's broken (e.g., a different color).
