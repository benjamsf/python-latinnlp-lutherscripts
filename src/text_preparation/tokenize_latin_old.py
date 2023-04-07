# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2a, tokenize prepared text by words
# (c) Benjam Bröijer, licensed under the MIT License

import os
import time
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

# Measure the start time
start_time = time.time()

# Tokenize the input_text using cltk_nlp
doc = cltk_nlp(input_text)

# Measure the end time
end_time = time.time()

# Calculate the time taken for tokenization
time_taken = end_time - start_time

# Calculate the number of tokens processed per second
tokens_per_second = len(doc.words) / time_taken
print(f"Tokens processed per second: {tokens_per_second}")

word_tokens = []

# Add a progress bar using tqdm
for i, word in enumerate(tqdm(doc.words, desc="Tokenizing words")):
    word_tokens.append(word.string)

print(word_tokens)

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write(' '.join(word_tokens))
# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
