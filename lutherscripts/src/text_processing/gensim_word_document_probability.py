import json
import os
import gensim
import pickle
import numpy as np

# Function to indicate documents by their metadata and list all words from the 
# dictionary with two probabilities: 
# 1) the probability to appear compared to the word's appearance in the whole corpus, 
# 2) the probability to appear compared to all words in this document. 

def main(corpus_path, dictionary_path, source_path, destination_path):
    
    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(corpus_path)

    # Load the dictionary from the file
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f, encoding='utf-8', fix_imports=True)

    # Load the tokenized text with metadata from source
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)

    # Calculate the number of documents in the corpus
    num_docs = len(corpus)

    # Calculate the total number of words in the corpus
    total_words = sum(cnt for doc in corpus for _, cnt in doc)

    # Create a dictionary to store the word probabilities per document
    word_probs = {}

    # Iterate over each document in the corpus
    for doc_idx, doc in enumerate(corpus):
        
        # Get the document metadata, if any
        metadata = tokenized_documents[doc_idx].get('metadata', {})
        
        # Iterate over each word in the document
        for word_id, cnt in doc:
            
            # Get the word and its total count in the corpus
            word = dictionary[word_id]
            word_total_count = dictionary.cfs[word_id]
            
            # Calculate the probability of the word appearing in the document
            word_doc_prob = cnt / sum(cnt for _, cnt in doc)
            
            # Calculate the probability of the word appearing in the corpus
            word_corpus_prob = word_total_count / total_words
            
            # Update the word probabilities dictionary with the document and corpus probabilities
            if word not in word_probs:
                word_probs[word] = []
            word_probs[word].append({
                'metadata': metadata,
                'doc_prob': word_doc_prob,
                'corpus_prob': word_corpus_prob
            })
    
    # Return the word probabilities dictionary
    return word_probs
