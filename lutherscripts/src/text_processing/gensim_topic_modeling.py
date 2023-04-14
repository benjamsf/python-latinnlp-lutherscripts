import json
import os
import gensim
import pickle
from gensim import corpora
from gensim.models import CoherenceModel
from tqdm import tqdm

def main(num_topics, num_passes, source_path, corpus_path, dictionary_path, destination_path):

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

    # Calculate topic distribution per topic
    doc_topic_distribution = []
    for tokenized_doc, bow in zip(tokenized_documents, corpus):
        doc_topics = lda_model.get_document_topics(bow, minimum_probability=0.0)
        topic_dict = {str(k): float(v) for k, v in doc_topics}
        if 'metadata' in tokenized_doc:
            doc_topic_distribution.append({'metadata': tokenized_doc['metadata'], **topic_dict})
        else:
            doc_topic_distribution.append(topic_dict)

    # Calculate word-topic distribution
    word_topic_distribution = {dictionary.get(token_id): lda_model.get_term_topics(token_id)
                               for token_id in dictionary.keys()}
    # Compute coherence score
    coherence_model = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='u_mass')
    coherence_score = coherence_model.get_coherence()

    # Save the results as a JSON file
    results = {
        'topics': topics,
        'topic_distribution': topic_distribution.tolist(),
        'doc_topic_distribution': [{k: float(v) if k != 'metadata' else v for k, v in doc_topics.items()} for doc_topics in doc_topic_distribution],
        'word_topic_distribution': {k: {w: float(p) for w, p in topic_probs} for k, topic_probs in word_topic_distribution.items()},
        'coherence_score': coherence_score
    }


    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The topic modeling results have been saved as {destination_path}')



