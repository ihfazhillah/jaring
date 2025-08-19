import os
import re
from pathlib import Path
from hijri_converter import Gregorian
import frontmatter

# Define paths
SOURCE_DIR = Path("../jaring-content").resolve()
DEST_DIR = Path("../jaring-content/converted").resolve()

# Create destination directory if it doesn't exist
DEST_DIR.mkdir(parents=True, exist_ok=True)

def convert_gregorian_to_hijri(gregorian_date_str):
    """Converts a Gregorian date string (YYYY-MM-DD) to Hijri (YYYY-MM-DD)."""
    try:
        year, month, day = map(int, gregorian_date_str.split('-'))
        gregorian_date = Gregorian(year, month, day)
        hijri_date = gregorian_date.to_hijri()
        return f"{hijri_date.year:04d}-{hijri_date.month:02d}-{hijri_date.day:02d}"
    except ValueError:
        print(f"Warning: Could not parse Gregorian date '{gregorian_date_str}'. Skipping Hijri conversion.")
        return gregorian_date_str # Return original if conversion fails

def convert_file(file_path, post_id_counter):
    """Converts a single content file to Jaring's format."""
    filename = file_path.name
    
    # Extract date and title from filename
    match = re.match(r'^(\d{4}-\d{2}-\d{2})(?:_\d{4})?\s(.+)\.md$', filename)
    if not match:
        print(f"Warning: Skipping '{filename}' due to unexpected filename format.")
        return None

    gregorian_date_str = match.group(1)
    title = match.group(2)
    
    hijri_date_str = convert_gregorian_to_hijri(gregorian_date_str)

    # Read original content
    original_content = file_path.read_text(encoding='utf-8')

    # Construct new frontmatter
    new_frontmatter = {
        "id": f"{hijri_date_str}-{post_id_counter:03d}", # Use sequential ID
        "title": title,
        "date": hijri_date_str, # Store Hijri date in metadata
        "type": "message", # Default type
        "tags": [] # No tags from filename
    }

    # Combine new frontmatter with original content
    # Use frontmatter library to dump, ensuring proper YAML formatting
    post = frontmatter.Post(original_content, handler=frontmatter.YAMLHandler(), **new_frontmatter)
    output_content = frontmatter.dumps(post)

    # Define new filename and path
    new_filename = f"{new_frontmatter['id']}-{title.replace(' ', '-')}.md"
    new_file_path = DEST_DIR / new_filename
    
    # Write the new file
    new_file_path.write_text(output_content, encoding='utf-8')
    print(f"Converted '{filename}' to '{new_file_path.name}'")
    return new_file_path

def main():
    print(f"Converting files from {SOURCE_DIR} to {DEST_DIR}")
    post_id_counter = 1
    for file_path in SOURCE_DIR.iterdir():
        if file_path.is_file() and file_path.suffix == '.md':
            converted_file = convert_file(file_path, post_id_counter)
            if converted_file:
                post_id_counter += 1
    print("Conversion complete.")

if __name__ == "__main__":
    main()
