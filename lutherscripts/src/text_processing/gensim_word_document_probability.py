import json
import os
import gensim
import pickle
import numpy as np


# Function to indicate documents by their metadata and list all words from the 
# dictionary with two probabilities: 
# 1) the probability to appear compared to the word's appearance in the whole corpus, 
# 2) the probability to appear compared to all words in this document. 

def main(source_path, corpus_path, dictionary_path, destination_path):
    
    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(corpus_path)

    # Check that the number of documents in the corpus matches the number of documents in the source file
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)
        num_docs_source = len(tokenized_documents)
        num_docs_corpus = len(corpus)
        if num_docs_corpus != num_docs_source:
            raise ValueError(f'The number of documents in the corpus ({num_docs_corpus}) does not match the number of documents in the source file ({num_docs_source})')
            
    # Load the dictionary from the file
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f, encoding='utf-8', fix_imports=True)

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
                word_probs[word] = {
                    'metadata': metadata,
                    'doc_probs': [],
                    'corpus_probs': []
                }
            word_probs[word]['doc_probs'].append(word_doc_prob)
            word_probs[word]['corpus_probs'].append(word_corpus_prob)

    # Flatten the list of document probabilities for each word
    doc_probs = [np.array(val['doc_probs']).flatten() for val in word_probs.values()]

    # Flatten the list of corpus probabilities for each word
    corpus_probs = [np.array(val['corpus_probs']).flatten() for val in word_probs.values()]

    # Calculate the mean values for the corpus and document probabilities
    corpus_mean_doc_prob = np.mean(np.concatenate(corpus_probs), axis=0)
    corpus_mean_corpus_prob = np.mean(np.concatenate(doc_probs), axis=0)

    # Create a list to store the document average probabilities and metadata
    doc_probs_list = []

    # Iterate over each document in the corpus and calculate the average probability
    for doc_idx, doc in enumerate(corpus):
        # Get the document metadata, if any
        metadata = tokenized_documents[doc_idx].get('metadata', {})
        # Calculate the total number of words in the document
        total_words = sum(cnt for _, cnt in doc)
        # Calculate the average probability for each document
        doc_avg_prob = sum([cnt / total_words for _, cnt in doc]) / len(doc)
        # Append the metadata and average probability to the list
        doc_probs_list.append({'metadata': metadata, 'doc_avg_prob': doc_avg_prob})

    # Sort the word probabilities from most probable to least probable
    sorted_word_probs = sorted(word_probs.items(), key=lambda x: np.mean(x[1]['corpus_probs']), reverse=True)

    # Create a list to store the word probability values
    word_probs_list = []

    # Iterate over each word in the sorted word probabilities list and store the word probability values
    for word, val in sorted_word_probs:
        # Calculate the average probability of the word in the corpus
        corpus_avg_prob = np.mean(val['corpus_probs'])
        # Calculate the average probability of the word per document in the corpus
        doc_avg_prob = np.mean(val['doc_probs'])
        # Append the word and its probabilities to the list
        word_probs_list.append({'word': word, 'corpus_avg_prob': corpus_avg_prob, 'doc_avg_prob': doc_avg_prob})

    # Sort the word probabilities list from most probable to least probable
    word_probs_list = sorted(word_probs_list, key=lambda x: x['corpus_avg_prob'], reverse=True)

    # Create a dictionary to store the mean values and sorted word probabilities
    mean_and_word_probs = {
        'Documents': doc_probs_list,
        'Words': word_probs_list
    }

    # Create a dictionary to store the mean values
    mean_values = {
        'Corpus': {
            'Average probability for a word to appear in this corpus': [float(corpus_mean_corpus_prob)],
            'Average probability for a word to appear per document in this corpus': [float(corpus_mean_doc_prob)]
        },
    }


    # Merge the mean values dictionary with the sorted word probabilities dictionary
    output_dict = {'mean_and_word_probs': mean_and_word_probs, 'mean_values': mean_values}

    # Save the output dictionary to a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=4)

    print(f'The word probability analysis results have been saved as {destination_path}')
