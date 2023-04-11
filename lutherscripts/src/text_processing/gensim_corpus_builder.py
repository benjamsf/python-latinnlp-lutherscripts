import json
import os
import gensim
import pickle
from gensim import corpora
from tqdm import tqdm

__author__ = "benjamsf"
__license__ = "MIT"

def main(source_path, destination_path):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)

    # Extract tokens from the tokenized_documents
    tokenized_text = [doc['tokens'] for doc in tokenized_documents]

    # Create a dictionary from the tokenized text
    dictionary = corpora.Dictionary(tqdm(tokenized_text, desc="Step 1 - Building dictionary:"))

    print("Dictionary before saving:")
    print(dictionary)
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

