import json
import os
import gensim
import pickle
import numpy as np
from lutherscripts.src.text_processing.gensim_LDA_tuner import tune_hyperparameters
from gensim import corpora
from gensim.models import CoherenceModel
from tqdm import tqdm

def main(num_topics, num_passes, num_iterations, source_path, corpus_path, dictionary_path, destination_path):

    num_topics = int(num_topics)
    num_passes = int(num_passes)

    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(corpus_path)

    # Load the dictionary from the file
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f, encoding='utf-8', fix_imports=True)
    
    # Load the tokenized text with metadata from source
    with open(source_path, 'r', encoding='utf-8') as f:
        tokenized_documents = json.load(f)
    
    # Load metadata from the tokenized source text
    metadata = [doc.get('metadata', {}) for doc in tokenized_documents]

    # Tune hyperparameters
    best_alpha, best_eta = tune_hyperparameters(num_topics, num_passes, num_iterations, source_path, corpus_path, dictionary_path)

    # Train the LDA model on the corpus with the best hyperparameters
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=dictionary,
                                        num_topics=num_topics,
                                        alpha=best_alpha,
                                        eta=best_eta,
                                        passes=num_passes)

    # Extract the topics and their associated words
    topics = []
    for topic_num, topic_words in tqdm(lda_model.show_topics(num_topics=num_topics, formatted=False),
                                        desc='Step 2 - Extracting topics:'):
        words = [{'word': word, 'probability': prob} for word, prob in topic_words]
        topic = {'topic_num': topic_num, 'words': words}
        topics.append(topic)

    # Map word IDs to their respective words
    id2word = dictionary.id2token

    # Calculate topic distribution (how probable it is for each word to appear in a topic)
    topic_distribution = []
    for topic_num, topic_prob in enumerate(lda_model.get_topics()):
        words_probs = [{'word': id2word[word_id], 'probability': prob} for word_id, prob in enumerate(topic_prob)]
        sorted_words_probs = sorted(words_probs, key=lambda x: x['probability'], reverse=True)
        topic_distribution.append({f'topic_{topic_num}': sorted_words_probs})

    # Create a dictionary of the word-topic distribution with words as keys
    word_topic_distribution = {}
    for topicid in range(lda_model.num_topics):
        topic_probs = lda_model.get_topic_terms(topicid)
        for word_id, prob in topic_probs:
            word = id2word[word_id]
            if word not in word_topic_distribution:
                word_topic_distribution[word] = {}
            word_topic_distribution[word][topicid] = float(prob)

    # Calculate topic distribution per topic
    doc_topic_distribution = []
    for tokenized_doc, bow in zip(tokenized_documents, corpus):
        doc_topics = lda_model.get_document_topics(bow, minimum_probability=0.0)
        topic_dict = {str(k): float(v) for k, v in doc_topics}
        if 'metadata' in tokenized_doc:
            doc_topic_distribution.append({'metadata': tokenized_doc['metadata'], **topic_dict})
        else:
            doc_topic_distribution.append(topic_dict)

    # Compute coherence scores
    coherence_model_umass = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='u_mass')
    coherence_model_cv = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_v')
    coherence_model_uci = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_uci')
    coherence_model_npmi = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_npmi')
    coherence_score_umass = coherence_model_umass.get_coherence()
    coherence_score_cv = coherence_model_cv.get_coherence()
    coherence_score_uci = coherence_model_uci.get_coherence()
    coherence_score_npmi = coherence_model_npmi.get_coherence()

    results = {
        'topics': topics,
        'topic_distribution': list(topic_distribution),
        'doc_topic_distribution': [{k: float(v) if k != 'metadata' else v for k, v in doc_topics.items()} for doc_topics in doc_topic_distribution],
        'word_topic_distribution': {k: {w: float(p) for w, p in topic_probs.items()} for k, topic_probs in word_topic_distribution.items()},
        'coherence_score': {
            'u_mass': coherence_score_umass,
            'c_v': coherence_score_cv,
            'c_uci': coherence_score_uci,
            'c_npmi': coherence_score_npmi
        },
        'metadata': metadata
    }

    def convert_float32_to_float(obj):
        if isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_float32_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_float32_to_float(item) for item in obj]
        else:
            return obj

    # Convert any float32 objects in the results dictionary to regular Python floats
    results = convert_float32_to_float(results)

    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The topic modeling results have been saved as {destination_path}')
