import io
import os
import re
import json
from cltk import NLP
from tqdm import tqdm
import logging
import sys
import io


def main(source_path, destination_path, progress_callback=None):
    # Instantiate a Latin-specific NLP object
    cltk_nlp = NLP(language="lat")

    logging.basicConfig(level=logging.INFO)

    # Load the Latin text from the source file
    input_file = os.path.abspath(source_path)
    logging.info(f"Reading input from file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # Split the input text into smaller chunks based on punctuation
    chunk_delimiters = r'[.!?]+'
    text_chunks = re.split(chunk_delimiters, input_text)

    # Process the text_chunks with cltk_nlp and update the progress bar
    sentence_tokens = []
    for chunk in tqdm(text_chunks, desc="Tokenizing sentences"):
        doc = cltk_nlp(chunk)
        for sentence in doc.sentences:
            sentence_text = ' '.join([word.string for word in sentence.words])
            sentence_tokens.append(sentence_text.strip())
        if progress_callback:
            progress_callback(len(sentence_tokens) / len(text_chunks))

        # Save the tokenized output to a JSON file
        output_file = os.path.abspath(destination_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sentence_tokens, f, ensure_ascii=False)

        # Print a message to confirm that the file has been saved
        print(f'The tokenized output has been saved as {output_file}')

