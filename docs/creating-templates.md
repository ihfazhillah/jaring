# How to Create a New Content Template

This document provides a step-by-step guide for creating new content type templates for the Jaring static site generator.

## 1. Naming Convention

To create a template for a new content type, you must follow a specific naming convention. The template file name must be:

`type_{your_type_name}.html`

Where `{your_type_name}` corresponds to the value you will use in the `type` field of your Markdown file's frontmatter.

**Examples:**
*   `type: quote` -> `templates/type_quote.html`
*   `type: image` -> `templates/type_image.html`
*   `type: video` -> `templates/type_video.html`

If a specific template for a type is not found, the system will automatically use `templates/message.html` as the default.

## 2. Template Location

All template files must be placed in the `templates/` directory at the root of the project.

## 3. Basic Structure & Extending `base.html`

To ensure a consistent look and feel across the entire site (including the header, footer, and CSS), all new templates should extend the `base.html` template.

The basic structure of a new template should be:

```jinja
{% extends "base.html" %}

{% block title %}{{ post.metadata.title }}{% endblock %}

{% block content %}
    <!-- Your custom HTML and Jinja2 logic goes here -->
{% endblock %}
```

## 4. Available Variables

Within your template, you have access to the `post` object, which contains all the information about the content being rendered.

*   `{{ post.metadata.title }}`: The title of the post.
*   `{{ post.metadata.tags }}`: A list of tags associated with the post.
*   `{{ post.metadata.og_image }}`: The path to the auto-generated Open Graph image.
*   `{{ post.date }}`: The date of the post.
*   `{{ post.html | safe }}`: The main content of the post, converted to HTML. Always use the `| safe` filter to ensure HTML is rendered correctly.
*   `{{ post.caption | safe }}`: The caption or "syarah" content (the text after the `---` delimiter), converted to HTML. Use the `| safe` filter here as well.

## 5. Handling Asset Paths with `depth`

The `depth` variable is crucial for ensuring that relative links to assets (like CSS files or images) work correctly, as the generated HTML files are located at different directory levels.

*   `depth` is an integer representing how many levels deep the current file is from the `output/` root.
*   **Usage:** Prepend `../` for each level of depth when creating a link.

**Example from `message.html`:**
```jinja
<link rel="stylesheet" href="{{ '../' * depth }}assets/style.css">
```
*   For the main `index.html`, `depth` is `0`, so the path becomes `assets/style.css`.
*   For a message page like `messages/1234.html`, `depth` is `1`, so the path becomes `../assets/style.css`.

## 6. Step-by-Step Example: Creating `type_image.html`

Let's create a template for a post where the image is the main focus.

**Step 1: Create the file `templates/type_image.html`**

**Step 2: Add the content to the file.**

This template will center the image and display the caption (which serves as the image's description) below it.

```jinja
{% extends "base.html" %}

{% block title %}{{ post.metadata.title }}{% endblock %}

{% block content %}
    <p><a href="{{ '../' * depth }}index.html">&larr; Kembali ke Daftar Pesan</a></p>
    <article class="message image-post">
        <h2>{{ post.metadata.title }}</h2>
        
        <div class="metadata">
            <span>Date: {{ post.date }}</span>
            {% if post.metadata.tags %}
                <span class="tags">
                    Tags:
                    {% for tag in post.metadata.tags %}
                        <a href="{{ '../' * depth }}tags/{{ tag }}.html">{{ tag }}</a>{% if not loop.last %}, {% endif %}
                    {% endfor %}
                </span>
            {% endif %}
        </div>

        <!-- Main content is the image itself -->
        <div class="content image-container">
             {{ post.html | safe }}
        </div>

        <!-- The caption is the primary text content -->
        {% if post.caption %}
        <div class="caption image-caption">
            {{ post.caption | safe }}
        </div>
        {% endif %}

    </article>
{% endblock %}
```

**Step 3: Create a new content file with `type: image`**

Create a file like `examples/nak/1447-02-05-image-post.md`:

```markdown
---
id: 1447-02-05-image-post
title: A Beautiful Scenery
type: image
tags:
  - nature
---

![A beautiful scenery](./path/to/your/image.jpg)

---

This is the description of the image. It will be displayed as a caption below the image.
```

When you run `python3 jaring.py`, this post will be rendered using the new `type_image.html` template.
