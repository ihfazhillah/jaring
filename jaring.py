import frontmatter
import jinja2
import markdown
import yaml
import re
from pictex import Canvas, Row, Column, Text
from pathlib import Path

def find_markdown_files(path):
    """Finds all markdown files in a given path."""
    return list(Path(path).glob("**/*.md"))

def generate_image_from_text(text_content, post_id, image_index):
    """Generates an image from text content using pictex and returns its relative path."""
    try:
        image_filename = f"{post_id}-{image_index}.png"
        image_path = Path("output/assets/images") / image_filename
        image_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists

        canvas = (
            Canvas()
            .color("#FFFFFF") # Global text color
            .background_color("#1DA1F2") # Twitter blue
            .padding(16) # Overall padding
            .border_radius(10) # Add border radius
        )

        tweet_card_content = Column(
            Text(text_content).font_size(18),
            Row(
                Text("Jaring").font_size(12),
            ).gap(10),
        ).gap(5)

        image = canvas.render(tweet_card_content)
        image.save(str(image_path))
        
        return f"assets/images/{image_filename}"

    except Exception as e:
        print(f"Error generating image for post {post_id} (index {image_index}): {e}")
        raise # Re-raise the exception as per user's request

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

def parse_file(file_path):
    """Parses a markdown file with frontmatter."""
    with open(file_path, "r") as f:
        post = frontmatter.load(f)
        date_parts = post.metadata.get("id", "").split("-")[:3]
        date = "-".join(date_parts)

        generated_images = [] # To store paths of generated images

        # Use FSM to parse notations and get modified content and extracted texts
        modified_content, extracted_image_texts = parse_img_notations_fsm(post.content)
        post.content = modified_content # Update post.content with the FSM's output

        for i, og_image_text in enumerate(extracted_image_texts):
            generated_image_path = generate_image_from_text(og_image_text, post.metadata['id'], i)
            generated_images.append(generated_image_path)

        # Set og_image to the first generated image's path, if any
        if generated_images:
            post.metadata["og_image"] = generated_images[0]
        else:
            post.metadata["og_image"] = None # Or handle as appropriate if no image is generated

        return {
            "metadata": post.metadata,
            "content": post.content,
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

def main():
    """Main function to generate the static site."""
    # Load configuration
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    content_path = config["content_path"]
    template_path = config["template_path"]
    output_path = Path(config["output_path"])

    # Create output directory if it doesn't exist
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
    
    posts = [parse_file(file) for file in files]

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
        html = render_html(template_env, "message.html", {"post": post, "depth": 1})
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

    # Generate tag index pages
    tags_output_dir = output_path / "tags"
    tags_output_dir.mkdir(exist_ok=True)

    for tag, tagged_posts in tags.items():
        tag_index_path = tags_output_dir / f"{tag}.html"
        html = render_html(template_env, "tag_index.html", {
            "tag": tag,
            "posts": tagged_posts,
            "depth": 1 # Depth for tag index pages is 1 (output/tags/tag.html)
        })
        save_html(tag_index_path, html)

    # Generate main index page with pagination
    posts_per_page = 20
    total_pages = (len(posts) + posts_per_page - 1) // posts_per_page

    for page_num in range(total_pages):
        start_index = page_num * posts_per_page
        end_index = start_index + posts_per_page
        paginated_posts = posts[start_index:end_index]

        if page_num == 0:
            index_file_name = "index.html"
        else:
            index_file_name = f"page-{page_num + 1}.html"

        main_index_path = output_path / index_file_name
        html = render_html(template_env, "index.html", {
            "posts": paginated_posts,
            "current_page": page_num + 1,
            "total_pages": total_pages,
            "depth": 0 # Depth for index pages is always 0
        })
        save_html(main_index_path, html)


if __name__ == "__main__":
    main()
