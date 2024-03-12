import os
import re
from tqdm import tqdm

def main(source_path, destination_path):
    # Ensure the destination directory exists
    os.makedirs(destination_path, exist_ok=True)

    with open(source_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Use regular expressions to find titles and split the text into documents
    documents = re.split(r'#\s*([^#]+)\s*#', text)

    # Remove any leading or trailing whitespace from titles and bodies
    documents = [d.strip() for d in documents]

    # Pair titles with bodies, excluding the first empty string (if any)
    pairs = [(documents[i], documents[i+1]) for i in range(0, len(documents), 2) if i+1 < len(documents)]

    # Process each document with a progress bar
    for i, (title, body) in tqdm(enumerate(pairs), total=len(pairs), desc="Processing documents"):
        # Make sure the title is safe to use as a filename
        filename_title = sanitize_filename(title)

        # Save each document as a separate .txt file, named after the title
        filename = os.path.join(destination_path, f'{filename_title}.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(body)  # Write only the body without the title inside the file

    print(f'The text has been exported to separate txt documents at {destination_path}.')

def sanitize_filename(title):
    """Remove disallowed characters and shorten the filename if necessary."""
    # Replace any characters not allowed in file names with underscores
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    # Shorten the title if it's too long for a filename
    return safe_title[:250]  # Filesystem limit, can be adjusted
