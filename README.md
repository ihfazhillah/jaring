# Jaring

Jaring is a simple, lightweight static site generator written in Python. It converts a collection of Markdown files into a clean, static HTML website. It's designed for creating and managing small, personal sites or blogs, with a focus on content ownership and simplicity.

## What's New (August 2025)

*   **Sitemap Generation:** Automatically creates a `sitemap.xml` file for better SEO.
*   **YouTube Video Embeds:** Automatically converts YouTube links into embedded iframes.
*   **Obsidian-style Callouts:** Supports `> [!NOTE]` style blockquotes.
*   **Improved Image Generation:**
    *   Text in generated images now wraps automatically.
    *   The author's name is now configurable in `jaring.yaml`.
*   **Responsive Images with Lightbox:** Images are now responsive and open in a full-screen lightbox when clicked.
*   **Image Compression:** All generated and copied images are automatically compressed for faster loading.

## Features

*   **Markdown-Based Content:** Write your posts in simple Markdown with YAML frontmatter.
*   **Static HTML Output:** Generates a fully static site that can be hosted anywhere.
*   **Jinja2 Templating:** Easily customize the look and feel of your site.
*   **Tagging System:** Organize your posts with tags and generate dedicated tag index pages.
*   **Pagination:** Automatically paginates your main index page.
*   **Text-to-Image Conversion:** Dynamically generate social media preview images from your text using the `!img{...}` notation.
*   **Web Share API Integration:** Mobile-friendly sharing using the native device UI.
*   **Configuration File:** Easily configure site parameters via `jaring.yaml`.

## Getting Started

### Prerequisites

*   Python 3.10 or higher

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ihfazhillah/jaring.git
    cd jaring
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate the static site, simply run the `jaring.py` script from the root of the project:

```bash
python3 jaring.py
```

You can also specify a custom configuration file:

```bash
python3 jaring.py -c /path/to/your/config.yaml
```

The generated HTML files will be placed in the `output/` directory.

## Project Structure

```
.
├── jaring.yaml         # Main configuration file
├── examples/           # Source content (Markdown files)
├── jaring.py           # The main Python script
├── output/             # Generated static site (ignored by git)
├── templates/          # Jinja2 templates for the site
└── requirements.txt    # Python dependencies
```

## Configuration

All site-wide settings are managed in the `jaring.yaml` file:

*   `site_name`: The name of your site, displayed in the header.
*   `site_url`: The full base URL of your site (e.g., `https://example.com`). Used for generating the sitemap.
*   `image_author_name`: The author name displayed on generated images.
*   `footer_text`: The text displayed in the footer.
*   `content_path`: The directory where your source Markdown files are located.
*   `template_path`: The directory where your Jinja2 templates are located.
*   `output_path`: The directory where the generated static site will be saved.

## Content Creation

To create a new post, add a new `.md` file to your content directory (e.g., `examples/nak/`).

### Frontmatter

Each file must begin with YAML frontmatter:

```yaml
---
id: 1447-02-04-new-post
title: My New Post
type: quote # Optional: e.g., quote, message. Defaults to 'message'.
tags:
  - python
  - static-site
---
```

*   `id`: A unique identifier for the post. The date-based format `YYYY-MM-DD-slug` is recommended for sorting.
*   `title`: The title of the post.
*   `type`: (Optional) The content type. This will determine which template is used to render the post (e.g., `type_quote.html`). If omitted, it defaults to `message`.
*   `tags`: A list of tags for the post.

### Captions and Explanations (Syarah)

To add a caption, explanation, or "syarah" to your main content, simply add a horizontal rule (`---`) to separate the main body from the caption. This works for any content type.

**Example:**

```markdown
This is the main content. It will be rendered normally.

---

This text is the caption or explanation. It will be displayed in a separate "syarah" section.
```

### Text-to-Image

To automatically generate a preview image for social sharing, use the `!img{...}` notation in your Markdown content. The text inside the curly braces will be rendered into a PNG image and linked in the post's metadata.

**Example:**

```markdown
!img{This text will become an image.}

This is the rest of your post content.
```

### Callouts

You can create styled blockquotes, similar to Obsidian, using the following syntax:

```markdown
> [!NOTE]
> This is a note.

> [!WARNING]
> This is a warning.
```
