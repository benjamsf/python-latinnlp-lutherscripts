# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2, tokenize prepared text by sentences
# (c) Benjam Bröijer, licensed under the MIT License

from cltk.tokenizers.sentence.lat import LatinPunktSentenceTokenizer
from tqdm import tqdm

sentence_tokenizer = LatinPunktSentenceTokenizer()

# Define the source and destination file names and paths
# Target text to projectfolder/txt/target_txt
# Output text to projectfolder/txt/output_txt
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_prepared_1.txt')
destination_path = os.path.join(script_path, '../../output/dsa_tokenized.pkl')

with open(source_path, 'r', encoding='utf-8') as file:
    input_text = file.read()

sentence_tokens = sentence_tokenizer.tokenize(input_text)
print(sentence_tokens)

# Split the input text into chunks (e.g., paragraphs) to process iteratively
chunks = input_text.split('\n\n')

# Initialize an empty list to store the tokenized sentences
sentence_tokens = []

# Process each chunk with a progress bar
for chunk in tqdm(chunks, desc="Tokenizing sentences"):
    # Tokenize the chunk by sentences
    chunk_sentences = sentence_tokenizer.tokenize(chunk)
    # Add the tokenized sentences to the list
    sentence_tokens.extend(chunk_sentences)

print(sentence_tokens)

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write(' '.join(output_doc.tokens))

# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
