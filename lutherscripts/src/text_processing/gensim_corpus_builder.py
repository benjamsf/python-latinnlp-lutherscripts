import json
import os
import gensim
import pickle
from gensim import corpora
from tqdm import tqdm

__author__ = "benjamsf"
__license__ = "MIT"

def main(source_path, destination_path, min_appearance=None, max_appearance=None):
    print(f"{source_path}, {destination_path}, {min_appearance}, {max_appearance}")
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)

    # Extract tokens from the tokenized_documents
    tokenized_text = [doc['tokens'] for doc in tokenized_documents]

    # Create a dictionary from the tokenized text
    dictionary = corpora.Dictionary(tqdm(tokenized_text, desc="Step 1 - Building dictionary:"))

    # Filter extremes from the dictionary only if min_appearance and max_appearance are provided
    if min_appearance is not None and max_appearance is not None:
        dictionary.filter_extremes(no_below=min_appearance, no_above=max_appearance, keep_n=None)

    print("First 10 items:", list(dictionary.items())[:10])

    dictionary_path = destination_path + '_dictionary.pkl'
    with open(dictionary_path, 'wb') as f:
        pickle.dump(dictionary, f, protocol=pickle.HIGHEST_PROTOCOL, fix_imports=True)

    # Convert the tokenized text into a corpus
    corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_text, desc="Step 2 - Building corpus:")]

    # Save the corpus as a market matrix
    corpus_path = destination_path + '_corpus.mm'
    gensim.corpora.MmCorpus.serialize(corpus_path, corpus)

    # Print a message to confirm that the corpus has been saved
    print(f'The corpus has been saved as {corpus_path}')
