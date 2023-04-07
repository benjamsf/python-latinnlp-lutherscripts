# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2, tokenize prepared text
# (c) Benjam Bröijer, licensed under the MIT License

import os
import string
from cltk import NLP
from tqdm import tqdm

# Instantiate a Latin-specific NLP object
cltk_nlp = NLP(language="lat")

# Define the source and destination file names and paths
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_prepared_2.txt')
destination_path = os.path.join(script_path, '../../output/dsa_tokenized2.pkl')

# Load the Latin text from the source file
with open(source_path, 'r', encoding='utf-8') as f:
    input_text = f.read()

# Remove punctuation marks from the input text
translator = str.maketrans("", "", string.punctuation)
input_text_no_punctuation = input_text.translate(translator)

# Split the input text into smaller chunks
text_chunks = input_text_no_punctuation.split()

# Process the text_chunks with cltk_nlp and update the progress bar
word_tokens = []
for chunk in tqdm(text_chunks, desc="Tokenizing words"):
    doc = cltk_nlp(chunk)
    for word in doc.words:
        word_tokens.append(word.string)

print(word_tokens)

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write(' '.join(word_tokens))
# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
