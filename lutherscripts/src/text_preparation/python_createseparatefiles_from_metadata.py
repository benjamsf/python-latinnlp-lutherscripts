import json
import os
from tqdm import tqdm  # Import the tqdm function for the progress bar

def sanitize_filename(title):
    """Remove disallowed characters and shorten the filename if necessary."""
    # Replace any characters not allowed in file names with underscores
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    # Shorten the title if it's too long for a filename
    return safe_title[:250]  # Filesystem limit, can be adjusted

def main(source_path, destination_path):
    # Ensure the destination directory exists
    os.makedirs(destination_path, exist_ok=True)
    
    # Load the corpus from JSON
    with open(source_path, 'r') as f:
        documents = json.load(f)

    # Process each document with a progress bar
    for i, document in tqdm(enumerate(documents), total=len(documents), desc="Processing documents"):
        # Extract the title ("metadata") and use it as the filename
        title = document.get('metadata', f'Document_{i}')  # Use a default title if missing
        # Convert tokens list to string, with commas
        body = ', '.join(document.get('tokens', []))
        
        # Make sure the title is safe to use as a filename
        filename_title = sanitize_filename(title)

        # Save each document as a separate .txt file, named after the title
        filename = os.path.join(destination_path, f'{filename_title}.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(body)  # Write only the body without the title inside the file

    print(f'The JSON has been exported to separate txt documents at {destination_path}.')

# Example usage
# main('source.json', 'destination_folder')
