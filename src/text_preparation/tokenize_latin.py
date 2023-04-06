# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Stage 2, tokenize prepared text
# (c) Benjam Bröijer, licensed under the MIT License

import os
from cltk import lat_models_cltk
from cltk.tokenizers import LatinTokenizationProcess
from cltk.core.data_types import Doc, Word
import nltk
nltk.download('punkt')
nltk.download('punkt')
nltk.download('lat_models_cltk')

from cltk.utils import CLTK_DATA_DIR
from cltk.core.data_types import LanguageModel

# Download the Latin sentence tokenizer
lat_models_cltk_sentence = LanguageModel(language='lat', model_name='lat_models_cltk')
lat_models_cltk_sentence_path = os.path.join(CLTK_DATA_DIR, 'lat/model/lat_models_cltk/tokenizers/sentence')
lat_models_cltk_sentence.download(destination_dir=lat_models_cltk_sentence_path)

# Define the source and destination file names and paths
# Target text to projectfolder/txt/target_txt
# Output text to projectfolder/txt/output_txt
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_prepared_1.txt')
destination_path = os.path.join(script_path, '../../output/dsa_tokenized.pkl')

# Load the Latin text from the source file
with open(source_path, 'r', encoding='utf-8') as f:
    input_text = f.read()

# Load the Latin tokenization process
tokenizer_process = LatinTokenizationProcess()

# Tokenize the input text
output_doc = tokenizer_process.run(input_doc=Doc(raw=input_text))

# Save the tokenized output to a file
with open(destination_path, 'w', encoding='utf-8') as f:
    f.write(' '.join(output_doc.tokens))
# Print a message to confirm that the file has been saved
print(f'The tokenized output has been saved as {destination_path}')
