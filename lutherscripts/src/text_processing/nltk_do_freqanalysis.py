import json
import os
import nltk
from nltk.probability import FreqDist
from collections import OrderedDict
from tqdm import tqdm


def main(source_path, destination_path, progress_callback=None):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_text = json.load(f)

    # Create a frequency distribution using NLTK with a progress bar
    fdist = FreqDist()
    for token in tqdm(tokenized_text, desc="Creating frequency distribution", unit="token"):
        fdist[token] += 1
        if progress_callback:
            progress_callback(fdist.N() / len(tokenized_text))

    # Sort the frequency distribution by frequency
    sorted_fdist = OrderedDict(fdist.most_common())

    # Save the frequency distribution as a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_fdist, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The frequency analysis has been saved as {destination_path}')


