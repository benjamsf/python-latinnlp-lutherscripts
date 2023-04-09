import json
import os
import nltk
from nltk import word_tokenize
from nltk.text import Text

__author__ = "benjamsf"
__license__ = "MIT"


def main(keyword, context_size, source_path, destination_path):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_text = f.read()

    # Create an NLTK Text object
    text = Text(nltk.word_tokenize(tokenized_text))

    # Perform KWIC analysis for the keyword
    kwic_results = list(text.concordance_list(keyword, lines=nltk.ConcordanceIndex(text.tokens).count(keyword), width=context_size))

    # Convert the KWIC results into JSON format
    kwic_json = []
    for result in kwic_results:
        kwic_json.append({
            "left_context": " ".join(result[0]),
            "keyword": result[1],
            "right_context": " ".join(result[2])
        })

    # Save the KWIC analysis as a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(kwic_json, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The KWIC analysis has been saved as {destination_path}')

