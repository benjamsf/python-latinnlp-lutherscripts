import json

# A little script to save documents from the json corpus as 
# separate files, for to work with certain 3rd party tools like Voyant


def save_documents_to_files(source_path, destination_path):
    # Load the corpus from json
    with open(source_path, 'r') as f:
        documents = json.load(f)

    for i, document in enumerate(documents):
        # Replace "metadata" with "title"
        document['title'] = document.pop('metadata')

        # Save each document as independent file
        with open(os.path.join(destination_path, f'document_{i}.json'), 'w') as f:
            json.dump(document, f)