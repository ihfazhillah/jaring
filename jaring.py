import frontmatter
import argparse
import jinja2
import markdown
import yaml
import re
import shutil
import textwrap
from pictex import Canvas, Row, Column, Text
from pathlib import Path
from PIL import Image

def find_markdown_files(path):
    """Finds all markdown files in a given path."""
    return list(Path(path).glob("**/*.md"))

def generate_image_from_text(text_content, post_id, image_index, author_name="Jaring"):
    """Generates an image from text content using pictex and returns its relative path."""
    try:
        image_filename = f"{post_id}-{image_index}.png"
        image_path = Path("output/assets/images") / image_filename
        image_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists

        # Wrap text
        wrapped_text = textwrap.fill(text_content, width=30)

        canvas = (
            Canvas()
            .color("#FFFFFF") # Global text color
            .background_color("#1DA1F2") # Twitter blue
            .padding(32) # Increased padding for a bigger image
            .border_radius(10)
        )

        tweet_card_content = Column(
            Text(wrapped_text).font_size(24), # Increased font size
            Row(
                Text(author_name).font_size(12),
            ).gap(10),
        ).gap(10)

        image = canvas.render(tweet_card_content)
        image.save(str(image_path))
        compress_image(image_path) # Compress the generated image
        
        return f"assets/images/{image_filename}"

    except Exception as e:
        print(f"Error generating image for post {post_id} (index {image_index}): {e}")
        raise # Re-raise the exception as per user's request

def compress_image(file_path):
    """Compresses an image file using Pillow."""
    try:
        img = Image.open(file_path)
        file_path_obj = Path(file_path)
        
        if file_path_obj.suffix.lower() in ['.jpg', '.jpeg']:
            img.save(file_path, 'JPEG', quality=85, optimize=True)
        elif file_path_obj.suffix.lower() == '.png':
            img.save(file_path, 'PNG', optimize=True)
            
    except Exception as e:
        print(f"Error compressing image {file_path}: {e}")

def copy_attachments(content, source_path, output_path):
    """
    Finds all markdown image references, copies them to the output assets 
    directory, and updates the content with the new paths.
    """
    # Regex to find all markdown image syntaxes
    img_regex = re.compile(r'![(.*?)](.*?)')
    
    def replace_path(match):
        alt_text = match.group(1)
        original_path_str = match.group(2)

        # If the path is a URL, do not process it.
        if original_path_str.startswith('http'):
            return match.group(0)
        
        # Create Path objects for easier manipulation
        original_path = Path(original_path_str)
        source_file_path = Path(source_path)
        
        # Determine the source of the image file
        # The path is relative to the markdown file, so resolve it
        image_source_path = (source_file_path.parent / original_path).resolve()
        
        # Define the destination path
        # We'll place it in an 'attachments' subdirectory to keep things clean
        destination_dir = Path(output_path) / 'assets' / 'attachments'
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct the final destination path for the image
        destination_file_path = destination_dir / image_source_path.name
        
        # Copy the file
        try:
            shutil.copy(image_source_path, destination_file_path)
            compress_image(destination_file_path) # Compress the image after copying
        except FileNotFoundError:
            print(f"Warning: Attachment not found at {image_source_path}")
            return match.group(0) # Return original if not found
        except Exception as e:
            print(f"Error copying attachment {image_source_path}: {e}")
            return match.group(0) # Return original on error

        # Calculate the new relative path for the HTML
        # This should be relative to the final HTML file's location
        new_relative_path = Path('..') / 'assets' / 'attachments' / image_source_path.name
        
        # Return the updated markdown image tag
        return f'![{alt_text}]({new_relative_path})'

    # Substitute all found image paths
    updated_content = img_regex.sub(replace_path, content)
    
    return updated_content

def parse_img_notations_fsm(content):
    modified_content_parts = []
    extracted_image_texts = []
    
    state = "NORMAL"
    current_img_text = []
    last_processed_idx = 0 # Tracks the index up to which content has been appended
    
    i = 0
    while i < len(content):
        char = content[i] # Define char at the beginning of each iteration

        # Check for '!img{' sequence
        if state == "NORMAL" and content[i:i+5] == '!img{':
            modified_content_parts.append(content[last_processed_idx:i]) # Append text before tag
            
            i += 5 # Move past '!img{'
            last_processed_idx = i # Update last processed index
            state = "IN_IMG_CONTENT"
            current_img_text = [] 
            continue # Skip to next iteration, 'i' is already updated, char will be new
        
        # Check for '}' sequence
        if state == "IN_IMG_CONTENT" and char == '}':
            extracted_image_texts.append("".join(current_img_text))
            modified_content_parts.append("".join(current_img_text)) # Append extracted text
            
            i += 1 # Move past '}'
            last_processed_idx = i # Update last processed index
            state = "NORMAL"
            continue # Skip to next iteration, 'i' is already updated, char will be new
            
        # Normal character processing (if no special sequence was found)
        # This part is reached if no 'continue' was executed above
        if state == "NORMAL":
            i += 1 # Just advance, char will be appended later when a tag is found or end of string
        elif state == "IN_IMG_CONTENT":
            current_img_text.append(char)
            i += 1
    
    # Append any remaining content after the last processed tag
    if last_processed_idx < len(content):
        modified_content_parts.append(content[last_processed_idx:])
    
    # Handle unclosed tag at the end of the content
    if state == "IN_IMG_CONTENT":
        # This means the tag was not closed. The content[last_processed_idx:]
        # would have already included the unclosed tag and its content.
        # So, no special action needed here for content reconstruction.
        pass
    
    final_content = "".join(modified_content_parts)
    
    return final_content, extracted_image_texts

def convert_youtube_links_to_iframes(content):
    """Converts YouTube links to iframe embeds."""
    # Regex for youtube.com/watch?v= and youtu.be/
    youtube_regex = re.compile(r'(https?://(?:www.)?(?:youtube.com/watch\?v=|youtu.be/)([\w-]+)([?&].*?)?)(\s*)')

    def replace_with_iframe(match):
        video_id = match.group(2)
        query_params = match.group(3) or '' # Capture query parameters
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}{query_params}" frameborder="0" allowfullscreen></iframe>'
    
    return youtube_regex.sub(replace_with_iframe, content)

def parse_obsidian_quotes(content):
    """Parses Obsidian-style callouts."""
    # Regex for > [!TYPE] [title] and subsequent quoted lines
    # It captures the type, an optional title, and the content block.
    callout_regex = re.compile(
        r'''^>\s*\[!(?P<type>\\w+)(?:\s+(?P<title>.*?))?\]\s*
(?P<content>(?:^>.*(?:\n|$))+)?''', re.DOTALL | re.MULTILINE
    )

    def replace_with_callout(match):
        callout_type = match.group('type').lower()
        callout_title = match.group('title')
        callout_content_raw = match.group('content')

        # Remove leading '> ' from each line of content
        processed_content = []
        if callout_content_raw:
            for line in callout_content_raw.splitlines():
                if line.startswith('> '):
                    processed_content.append(line[2:])
                else:
                    processed_content.append(line) # Should not happen with current regex, but for safety

        # Convert the processed content to HTML
        callout_html_content = convert_markdown_to_html('\n'.join(processed_content).strip())

        # Construct the HTML for the callout
        html_output = f'<div class="callout {callout_type}">'
        
        # Add title if present
        if callout_title:
            html_output += f'<div class="callout-title"><div class="callout-title-inner">{callout_title.strip()}</div></div>'
        
        html_output += f'<div class="callout-content">{callout_html_content}</div>'
        html_output += '</div>'
        
        return html_output

    return callout_regex.sub(replace_with_callout, content)

def parse_file(file_path, output_path, author_name):

    """Parses a markdown file with frontmatter."""
    with open(file_path, "r") as f:
        post = frontmatter.load(f)
        date_parts = post.metadata.get("id", "").split("-")[:3]
        date = "-".join(date_parts)

        generated_images = [] # To store paths of generated images

        # Handle content and caption separation
        parts = post.content.split('---', 1)
        main_content = parts[0]
        caption_content = parts[1] if len(parts) > 1 else None

        # Copy attachments and update content paths
        main_content = copy_attachments(main_content, file_path, output_path)
        if caption_content:
            caption_content = copy_attachments(caption_content, file_path, output_path)

        # Convert YouTube links to iframes
        main_content = convert_youtube_links_to_iframes(main_content)
        if caption_content:
            caption_content = convert_youtube_links_to_iframes(caption_content)

        # Parse obsidian quotes
        main_content = parse_obsidian_quotes(main_content)
        if caption_content:
            caption_content = parse_obsidian_quotes(caption_content)

        # Use FSM to parse notations and get modified content and extracted texts
        modified_content, extracted_image_texts = parse_img_notations_fsm(main_content)
        post.content = modified_content # Update post.content with the FSM's output

        if caption_content:
            post.caption = convert_markdown_to_html(caption_content.strip())
        else:
            post.caption = None

        for i, og_image_text in enumerate(extracted_image_texts):
            generated_image_path = generate_image_from_text(og_image_text, post.metadata['id'], i, author_name)
            generated_images.append(generated_image_path)

        # Set og_image to the first generated image's path, if any
        if generated_images:
            post.metadata["og_image"] = generated_images[0]
        else:
            post.metadata["og_image"] = None # Or handle as appropriate if no image is generated

        return {
            "metadata": post.metadata,
            "content": post.content,
            "caption": post.caption,
            "path": file_path,
            "date": date,
            # "og_image_text": og_image_text, # This is no longer needed in the return dict
        }


def convert_markdown_to_html(content):
    """Converts markdown content to HTML."""
    return markdown.markdown(content)

def render_html(template_env, template_name, context):
    """Renders a Jinja2 template."""
    template = template_env.get_template(template_name)
    return template.render(context)

def save_html(file_path, html):
    """Saves HTML content to a file."""
    with open(file_path, "w") as f:
        f.write(html)

from datetime import datetime

def generate_sitemap(posts, output_path, site_url):
    """Generates a sitemap.xml file."""
    sitemap_path = Path(output_path) / "sitemap.xml"
    now = datetime.now().strftime("%Y-%m-%d")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'


    for post in posts:
        post_id = post["metadata"]["id"]
        url = f"{site_url}/messages/{post_id}.html"
        xml += f'  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{now}</lastmod>\n'
        xml += f'  </url>\n'

    xml += '</urlset>'

    with open(sitemap_path, "w") as f:
        f.write(xml)

def main():
    """Main function to generate the static site."""
    posts_per_page = 10 # Define globally for all pagination
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Generate a static site from markdown files.")
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=None,
        help="Path to the custom configuration file"
    )
    args = parser.parse_args()

    if args.config:
        config_path = Path(args.config)
    else:
        config_path = Path("jaring.yaml")
        if not config_path.is_file():
            config_path = Path("config.yaml") # Fallback for old name

    # Load configuration
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file '{config_path}': {e}")
        exit(1)

    content_path = config["content_path"]
    template_path = config["template_path"]
    output_path = Path(config["output_path"])

    # Create output directory if it's not exist
    assets_path = output_path / "assets"
    assets_path.mkdir(exist_ok=True)
    output_path.mkdir(exist_ok=True)

    # Copy static files
    with open(f"{template_path}/style.css", "r") as f:
        css_content = f.read()
    with open(assets_path / "style.css", "w") as f:
        f.write(css_content)

    # Setup Jinja2 environment
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path)
    )
    template_env.globals['site_name'] = config['site_name']
    template_env.globals['footer_text'] = config['footer_text']
    template_env.filters['split'] = lambda value, delimiter: value.split(delimiter)

    # Pipeline
    files = find_markdown_files(content_path)
    
    posts = [parse_file(file, output_path, config.get('image_author_name', 'Jaring')) for file in files]

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p['metadata']['id'], reverse=True)

    for post in posts:
        # Replace single newlines with double newlines to create paragraphs
        content_with_paragraphs = post["content"].replace('\n', '\n\n')
        post["html"] = convert_markdown_to_html(content_with_paragraphs)

    # Generate individual message pages
    for post in posts:
        post_id = post["metadata"]["id"]
        post_output_dir = output_path / "messages"
        post_output_dir.mkdir(parents=True, exist_ok=True)
        
        post_output_path = post_output_dir / f"{post_id}.html"

        # Temporarily add post to globals for base.html
        template_env.globals['post'] = post

        # Get content type, default to 'message' if not specified
        content_type = post["metadata"].get("type", "message")
        template_name = f"type_{content_type}.html"

        try:
            # Try to get the specific template
            template_to_render = template_env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound:
            # Fallback to the default message.html
            template_to_render = template_env.get_template("message.html")

        html = template_to_render.render({"post": post, "depth": 1})
        del template_env.globals['post'] # Clean up
        save_html(post_output_path, html)

    # Collect all tags and associated posts
    tags = {}
    for post in posts:
        post_tags = post["metadata"].get("tags", [])
        for tag in post_tags:
            if tag not in tags:
                tags[tag] = []
            tags[tag].append(post)

    # Generate tag index pages with pagination
    tags_output_dir = output_path / "tags"
    tags_output_dir.mkdir(exist_ok=True)

    for tag, tagged_posts in tags.items():
        total_pages = (len(tagged_posts) + posts_per_page - 1) // posts_per_page

        # Generate the main tag page
        tag_index_path = tags_output_dir / f"{tag}.html"
        html = render_html(template_env, "tag_index.html", {
            "tag": tag,
            "posts": tagged_posts[:posts_per_page],
            "total_pages": total_pages,
            "depth": 1
        })
        save_html(tag_index_path, html)

        # Generate partial pages for the tag
        for page_num in range(1, total_pages):
            start_index = page_num * posts_per_page
            end_index = start_index + posts_per_page
            paginated_posts = tagged_posts[start_index:end_index]

            partial_page_path = tags_output_dir / f"{tag}-page-{page_num + 1}.html"
            html = render_html(template_env, "post_cards.html", {
                "posts": paginated_posts,
                "depth": 1
            })
            save_html(partial_page_path, html)

    # New logic for partial page generation for main index
    total_pages = (len(posts) + posts_per_page - 1) // posts_per_page

    # Generate the main index.html with the first page of posts
    main_index_path = output_path / "index.html"
    html = render_html(template_env, "index.html", {
        "posts": posts[:posts_per_page],
        "tags": sorted(tags.keys()),
        "total_pages": total_pages,
        "depth": 0
    })
    save_html(main_index_path, html)

    # Generate partial HTML files for subsequent pages for main index
    for page_num in range(1, total_pages):
        start_index = page_num * posts_per_page
        end_index = start_index + posts_per_page
        paginated_posts = posts[start_index:end_index]

        partial_page_path = output_path / f"page-{page_num + 1}.html"
        html = render_html(template_env, "post_cards.html", {
            "posts": paginated_posts,
            "depth": 0 # Partials are loaded from the root
        })
        save_html(partial_page_path, html)

    # Generate sitemap
    generate_sitemap(posts, output_path, config['site_url'])

if __name__ == "__main__":
    main()