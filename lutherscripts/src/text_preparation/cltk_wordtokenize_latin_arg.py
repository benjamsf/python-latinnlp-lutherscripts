import os
import string
import json
from cltk import NLP
from tqdm import tqdm
import logging
import sys
import io
from cltk.stops.lat import STOPS as LATIN_STOPS
from lutherscripts.src.data.extrastopwords import extrastopwords_lat as EXTRA_STOPS
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

    # Split the input text into documents
    input_documents = re.split(r'(?<=#end#)', input_text, flags=re.IGNORECASE)

    document_tokens = []

    for document in input_documents:
        if not document.strip():
            continue

        # Extract metadata from the document
        metadata = re.search(r'#(.*?)#', document).group(1)

        # Remove metadata from the document
        document = re.sub(r'#.*?#', '', document)

        # Convert the document text to lowercase
        document = document.lower()

        # Remove punctuation marks, digits, and special characters from the document
        document_no_punctuation = re.sub(r'[^\w\s]', '', document)
        document_no_digits = re.sub(r'\d+', '', document_no_punctuation)

        # Split the document into smaller chunks
        text_chunks = document_no_digits.split()

        # Process the text_chunks with cltk_nlp and update the progress bar
        word_tokens = []
        for chunk in tqdm(text_chunks, desc=f"Tokenizing words for document: {metadata}", file=sys.stdout):
            doc = cltk_nlp(chunk)
            for word in doc.words:
                lemma = latin_lemmatizer.lemmatize([word.string])[0][1].lower()
                if lemma not in LATIN_STOPS and lemma not in EXTRA_STOPS and len(lemma) > 2:
                    word_tokens.append(lemma)

        document_tokens.append({"metadata": metadata, "tokens": word_tokens})

    # Save the tokenized output to a JSON file
    output_file = os.path.abspath(destination_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(document_tokens, f, ensure_ascii=False)

    # Print a message to confirm that the file has been saved
    print(f'The tokenized output has been saved as {destination_path}')




