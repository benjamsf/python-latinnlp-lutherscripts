# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2, tokenize prepared text
# (c) Benjam Bröijer, licensed under the MIT License

import os
from cltk import NLP
from cltk.tokenizers.word import WordTokenizer


# Instantiate a Latin-specific NLP object
cltk_nlp = NLP(language="lat")



# Define the source and destination file names and paths
# Target text to projectfolder/txt/target_txt
# Output text to projectfolder/txt/output_txt
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_prepared_2.txt')
destination_path = os.path.join(script_path, '../../output/dsa_tokenized2.pkl')

# Load the Latin text from the source file
with open(source_path, 'r', encoding='utf-8') as f:
    input_text = f.read()

doc = cltk_nlp(input_text)
word_tokens = [word.string for word in doc.words]
print(word_tokens)

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write(' '.join(word_tokens))
# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
