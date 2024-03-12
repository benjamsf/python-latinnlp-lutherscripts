import json
from nltk.probability import FreqDist
from tqdm import tqdm

def main(source_path, destination_path):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # Create a frequency distribution using NLTK with a progress bar
    fdist = FreqDist()
    for document in tqdm(documents, desc="Creating frequency distribution", unit="document"):
        # Extract tokens from each document
        tokens = document.get('tokens', [])  # Ensure there's a default empty list if 'tokens' is missing
        for token in tokens:
            # Increment the count for each token
            fdist[token] += 1

    # Convert the frequency distribution to a dictionary for JSON serialization
    fdist_dict = {word: freq for word, freq in fdist.items()}

    # Save the frequency distribution as a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(fdist_dict, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The frequency analysis has been saved as {destination_path}')

if __name__ == '__main__':
    # Example usage
    main('source.json', 'destination.json')

