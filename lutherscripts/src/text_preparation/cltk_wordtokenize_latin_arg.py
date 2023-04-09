import os
import string
import json
from cltk import NLP
from tqdm import tqdm
import logging
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main(source_path, destination_path):
    
    logging.basicConfig(level=logging.INFO)
    # Instantiate a Latin-specific NLP object
    cltk_nlp = NLP(language="lat")

    input_file = os.path.abspath(source_path)

    # Load the Latin text from the source file
    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # Remove punctuation marks from the input text
    translator = str.maketrans("", "", string.punctuation)
    input_text_no_punctuation = input_text.translate(translator)

    # Split the input text into smaller chunks
    text_chunks = input_text_no_punctuation.split()

    # Process the text_chunks with cltk_nlp and update the progress bar
    word_tokens = []
    for chunk in tqdm(text_chunks, desc="Tokenizing words"):
        doc = cltk_nlp(chunk)
        for word in doc.words:
            word_tokens.append(word.string)

    print(word_tokens)

    # Save the tokenized output to a JSON file
    output_file = os.path.abspath(destination_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(word_tokens, f, ensure_ascii=False)

    # Print a message to confirm that the file has been saved
    print(f'The tokenized output has been saved as {destination_path}')

