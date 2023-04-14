import numpy as np
from gensim.models import CoherenceModel
import gensim
import pickle
import json
from tqdm import tqdm
from random import randint, uniform

# function to automatically tune hyperparameters alpha and eta for the LDA Topic Modeler
# implementation: random search, needs the input of iterations to be tried

def tune_hyperparameters(num_topics, num_passes, num_iterations, source_path, corpus_path, dictionary_path):
    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(corpus_path)

    # Load the dictionary from the file
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f, encoding='utf-8', fix_imports=True)

    # Load the tokenized text with metadata from source
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)

    # Define the hyperparameter space for alpha and eta
    alpha_space = [uniform(0.01, 1.0) for i in range(num_iterations)]
    eta_space = [uniform(0.01, 1.0) for i in range(num_iterations)]

    # Initialize a list to store the coherence scores for each combination of hyperparameters
    coherence_scores = []

    # Loop over all iterations of random search
    for i in tqdm(range(num_iterations), desc='Performing random search for LDA alpha and eta'):
        # Select a random alpha and eta value from the hyperparameter space
        alpha = alpha_space[i]
        eta = eta_space[i]

        # Train the LDA model on the corpus with the current hyperparameters
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=num_topics,
                                               alpha=alpha,
                                               eta=eta,
                                               passes=num_passes)

        # Compute the coherence score for the current hyperparameters
        coherence_model_umass = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='u_mass')
        coherence_model_cv = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_v')
        coherence_model_uci = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_uci')
        coherence_model_npmi = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_npmi')
        coherence_score_umass = coherence_model_umass.get_coherence()
        coherence_score_cv = coherence_model_cv.get_coherence()
        coherence_score_uci = coherence_model_uci.get_coherence()
        coherence_score_npmi = coherence_model_npmi.get_coherence()
        avg_coherence_score = (coherence_score_umass + coherence_score_cv + coherence_score_uci + coherence_score_npmi) / 4

        # Append the coherence score to the list of scores
        coherence_scores.append((alpha, eta, avg_coherence_score))

    # Find the hyperparameters with the highest coherence score
    best_alpha, best_eta, best_score = max(coherence_scores, key=lambda x: x[2])

    # Print the best hyperparameters and their coherence score
    print(f'Best alpha: {best_alpha}, best eta: {best_eta}, best coherence score achieved: {best_score}')

    return best_alpha, best_eta

