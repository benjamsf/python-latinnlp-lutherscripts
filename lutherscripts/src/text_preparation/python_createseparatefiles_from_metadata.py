import json
import os
from tqdm import tqdm  # Import the tqdm function for the progress bar

def main(source_path, destination_path):
    # Ensure the destination directory exists
    os.makedirs(destination_path, exist_ok=True)
    
    # Load the corpus from JSON
    with open(source_path, 'r') as f:
        documents = json.load(f)

    # Process each document with a progress bar
    for i, document in tqdm(enumerate(documents), total=len(documents), desc="Processing documents"):
        # Extract the title ("metadata") and the document body ("tokens")
        title = document.get('metadata', f'Document {i}')  # Use a default title if missing
        body = ', '.join(document.get('tokens', []))  # Convert tokens list to string, with commas

        # Combine the title and the body with two newlines in between
        content = f"{title}\n\n{body}"

        # Save each document as a separate .txt file
        filename = os.path.join(destination_path, f'document_{i}.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f'The JSON has been exported to separate txt documents at {destination_path}.')

