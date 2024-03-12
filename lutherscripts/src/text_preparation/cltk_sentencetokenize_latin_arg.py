import os
import re
import sys
import json
from cltk import NLP
from tqdm import tqdm
import logging
from cltk.stops.lat import STOPS as LATIN_STOPS
from lutherscripts.src.data.extrastopwords import extrastopwords_lat as EXTRA_STOPS
from cltk.lemmatize.lat import LatinBackoffLemmatizer

def main(source_path, destination_path, progress_callback=None):
    logging.basicConfig(level=logging.INFO)

    # Instantiate a Latin-specific NLP object
    cltk_nlp = NLP(language="lat")

    # Instantiate a Latin-specific lemmatizer
    latin_lemmatizer = LatinBackoffLemmatizer()

    input_file = os.path.abspath(source_path)
    logging.info(f"Reading input from file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # Split the input text into documents
    input_documents = re.split(r'(?<=#end#)', input_text, flags=re.IGNORECASE)

    document_sentences = []

    for document in tqdm(input_documents, desc="Processing documents", file=sys.stdout):
        if not document.strip():
            continue

        # Extract metadata from the document
        metadata = re.search(r'#(.*?)#', document).group(1)

        # Remove metadata from the document
        document_text = re.sub(r'#.*?#', '', document)

        # Convert the document text to lowercase
        document_text = document_text.lower()

        # Remove punctuation marks, digits, and special characters from the document
        document_no_punctuation = re.sub(r'[^\w\s]', '', document_text)
        document_no_digits = re.sub(r'\d+', '', document_no_punctuation)

        # Tokenize the document into sentences
        doc = cltk_nlp(document_no_digits)

        cleaned_sentences = []
        for sentence in doc.sentences:
            # Lemmatize and remove stopwords from each sentence
            lemmatized_words = [
                latin_lemmatizer.lemmatize([word.string])[0][1].lower()
                for word in sentence.words
                if word.string.lower() not in LATIN_STOPS and word.string.lower() not in EXTRA_STOPS
            ]
            cleaned_sentence = ' '.join(lemmatized_words).strip()
            if cleaned_sentence:  # Ensure the sentence is not empty
                cleaned_sentences.append(cleaned_sentence)

        # Append the processed sentences along with metadata
        document_sentences.append({"metadata": metadata, "sentences": cleaned_sentences})

    # Save the tokenized and lemmatized output to a JSON file
    output_file = os.path.abspath(destination_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(document_sentences, f, ensure_ascii=False)

    # Print a message to confirm that the file has been saved
    print(f'The tokenized and lemmatized output has been saved as {output_file}')

if __name__ == '__main__':
    # Example usage
    main('source.json', 'destination.json')
