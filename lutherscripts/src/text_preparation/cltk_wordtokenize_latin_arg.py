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
    cltk_nlp = NLP(language="lat")
    latin_lemmatizer = LatinBackoffLemmatizer()

    input_file = os.path.abspath(source_path)

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    input_documents = re.split(r'(?<=#end#)', input_text, flags=re.IGNORECASE)

    document_tokens = []

    for document in tqdm(input_documents, desc="Processing documents", unit="document", file=sys.stdout):
        if not document.strip():
            continue

        metadata_match = re.search(r'#(.*?)#', document)
        metadata = metadata_match.group(1) if metadata_match else ""
        document_text = re.sub(r'#.*?#', '', document)
        document_text = document_text.lower()
        document_text = re.sub(r'[^\w\s]', '', document_text)

        word_tokens = []
        # Process each word in the document_text
        words = document_text.split()
        for word in tqdm(words, desc=f"Tokenizing {metadata}", unit="token", leave=False, file=sys.stdout):
            cleaned_word = re.sub(r'\d+', '', word)
            if not cleaned_word:
                continue
            
            doc = cltk_nlp(cleaned_word)
            for processed_word in doc.words:
                lemma = latin_lemmatizer.lemmatize([processed_word.string])[0][1].lower()
                cleaned_lemma = re.sub(r'\d+', '', lemma)
                if cleaned_lemma and cleaned_lemma not in LATIN_STOPS and cleaned_lemma not in EXTRA_STOPS and len(cleaned_lemma) > 1:
                    word_tokens.append(cleaned_lemma)

        document_tokens.append({"metadata": metadata, "tokens": word_tokens})

    output_file = os.path.abspath(destination_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(document_tokens, f, ensure_ascii=False)

    print(f'The tokenized output has been saved as {destination_path}')

if __name__ == '__main__':
    main('source.json', 'destination.json')