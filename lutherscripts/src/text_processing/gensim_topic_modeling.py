import json
import os
import gensim
import pickle
from gensim import corpora
from tqdm import tqdm

import json
import os
import gensim
import pickle
from gensim import corpora
from gensim.models import CoherenceModel
from tqdm import tqdm

def main(num_topics, num_passes, source_path, dictionary_path, destination_path):

    num_topics = int(num_topics)
    num_passes = int(num_passes)

    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(source_path)

    # Load the dictionary from the file
    with open(dictionary_path, 'rb') as f:
        dictionary = pickle.load(f, encoding='utf-8', fix_imports=True)

    # Train the LDA model on the corpus
    with tqdm(desc="Step 1 - Training LDA model:", total=num_passes) as pbar:
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=num_topics,
                                               passes=num_passes)

    # Extract the topics and their associated words
    topics = []
    for topic_num, topic_words in tqdm(lda_model.show_topics(num_topics=num_topics, formatted=False),
                                        desc='Step 2 - Extracting topics:'):
        words = [word for word, _ in topic_words]
        topics.append({'topic_num': topic_num, 'words': words})

    # Calculate topic distribution
    topic_distribution = lda_model.get_topics()

    # Calculate document-topic distribution
    doc_topic_distribution = [lda_model.get_document_topics(doc) for doc in corpus]

    # Calculate word-topic distribution
    word_topic_distribution = {dictionary.get(token_id): lda_model.get_term_topics(token_id)
                               for token_id in dictionary.keys()}

    # Compute coherence score
    coherence_model = CoherenceModel(model=lda_model, texts=corpus, dictionary=dictionary, coherence='u_mass')
    coherence_score = coherence_model.get_coherence()

    # Save the results as a JSON file
    results = {
        'topics': topics,
        'topic_distribution': topic_distribution.tolist(),
        'doc_topic_distribution': [dict(doc_topics) for doc_topics in doc_topic_distribution],
        'word_topic_distribution': word_topic_distribution,
        'coherence_score': coherence_score
    }

    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The topic modeling results have been saved as {destination_path}')



