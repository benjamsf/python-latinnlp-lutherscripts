import os
import string
import json
from cltk import NLP
from tqdm import tqdm
import logging
import sys
import io
from cltk.stops.lat import STOPS as LATIN_STOPS
from cltk.lemmatize.lat import LatinBackoffLemmatizer
import re


def main(source_path, destination_path, progress_callback=None):
    logging.basicConfig(level=logging.INFO)
    # Instantiate a Latin-specific NLP object
    cltk_nlp = NLP(language="lat")

    # Instantiate a Latin-specific lemmatizer
    latin_lemmatizer = LatinBackoffLemmatizer()

    input_file = os.path.abspath(source_path)

    # Load the Latin text from the source file
    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # Convert the text to lowercase
    input_text = input_text.lower()

    # Remove punctuation marks, digits, and special characters from the input text
    input_text_no_punctuation = re.sub(r'[^\w\s]', '', input_text)
    input_text_no_digits = re.sub(r'\d+', '', input_text_no_punctuation)

    # Split the input text into smaller chunks
    text_chunks = input_text_no_digits.split()

    # Process the text_chunks with cltk_nlp and update the progress bar
    word_tokens = []
    for chunk in tqdm(text_chunks, desc="Tokenizing words", file=sys.stdout):
        doc = cltk_nlp(chunk)
        for word in doc.words:
            lemma = latin_lemmatizer.lemmatize([word.string])[0][1].lower()
            if lemma not in LATIN_STOPS and len(lemma) > 2:
                word_tokens.append(lemma)

    # Save the tokenized output to a JSON file
    output_file = os.path.abspath(destination_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([word_tokens], f, ensure_ascii=False)

    # Print a message to confirm that the file has been saved
    print(f'The tokenized output has been saved as {destination_path}')


