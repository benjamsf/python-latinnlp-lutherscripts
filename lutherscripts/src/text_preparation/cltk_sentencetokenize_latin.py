# Python script to prepare Latin text from UTF-8 textfile to form usable in NLP
# Stage 2b, tokenize prepared text by sentences
# (c) Benjam Bröijer, licensed under the MIT License

import os
import re
from cltk import NLP
from tqdm import tqdm

# Instantiate a Latin-specific NLP object
cltk_nlp = NLP(language="lat")

# Define the source and destination file names and paths
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_prepared_1.txt')
destination_path = os.path.join(script_path, '../../output/dsa_tokenized.pkl')

# Load the Latin text from the source file
with open(source_path, 'r', encoding='utf-8') as f:
    input_text = f.read()

# Split the input text into smaller chunks based on punctuation
chunk_delimiters = r'[.!?]+'
text_chunks = re.split(chunk_delimiters, input_text)

# Process the text_chunks with cltk_nlp and update the progress bar
sentence_tokens = []
for chunk in tqdm(text_chunks, desc="Tokenizing sentences"):
    doc = cltk_nlp(chunk)
    for sentence in doc.sentences:
        sentence_text = ' '.join([word.string for word in sentence.words])
        sentence_tokens.append(sentence_text.strip())

print(sentence_tokens)

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sentence_tokens))
# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
