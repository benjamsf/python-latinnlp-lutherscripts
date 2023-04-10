import json
import os
import gensim
from gensim import corpora
from tqdm import tqdm

__author__ = "benjamsf"
__license__ = "MIT"

def main(source_path, destination_path):
    # Load the tokenized text from the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_text = json.load(f)

    # Create a dictionary from the tokenized text
    dictionary = corpora.Dictionary(tqdm(tokenized_text, desc="Step 1 - Building dictionary:"))

    # Save the dictionary
    dictionary_path = destination_path + '_dictionary'
    with open(dictionary_path, 'w', encoding='utf-8') as f:
        dictionary.save(f, separately=['id2token'])

    # Convert the tokenized text into a corpus
    corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_text, desc="Step 2 - Building corpus:")]

    # Save the corpus as a market matrix
    corpus_path = destination_path + '_corpus'
    gensim.corpora.MmCorpus.serialize(corpus_path, corpus)

    # Print a message to confirm that the corpus has been saved
    print(f'The corpus has been saved as {corpus_path}')
