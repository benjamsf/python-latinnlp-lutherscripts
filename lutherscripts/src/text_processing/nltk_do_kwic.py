import json
import os
import nltk
from nltk.text import Text
from tqdm import tqdm

__author__ = "benjamsf"
__license__ = "MIT"


def main(keyword, context_size, source_path, destination_path, progress_callback=None):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_text = f.read()

    # Create an NLTK Text object
    text = Text(nltk.word_tokenize(tokenized_text))

    # Perform KWIC analysis for the keyword
    concordance = nltk.ConcordanceIndex(text.tokens)
    kwic_results = []
    keyword_occurrences = concordance.offsets(keyword)
    for index in tqdm(keyword_occurrences, desc="Analyzing keyword occurrences"):
        left_context = text.tokens[index-context_size:index]
        right_context = text.tokens[index+len(keyword):index+len(keyword)+context_size]
        kwic_results.append({
            "left_context": " ".join(left_context),
            "keyword": keyword,
            "right_context": " ".join(right_context)
        })
        if progress_callback:
            progress_callback(len(kwic_results) / len(keyword_occurrences))

    # Convert the KWIC results into JSON format
    kwic_json = json.dumps(kwic_results, ensure_ascii=False, indent=2)

    # Save the KWIC analysis as a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        f.write(kwic_json)

    # Print a message to confirm that the file has been saved
    print(f'The KWIC analysis has been saved as {destination_path}')


