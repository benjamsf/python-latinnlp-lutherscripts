import json
import os
import nltk
from nltk import word_tokenize
from nltk.text import Text

__author__ = "benjamsf"
__license__ = "MIT"

# Define the source and destination file names and paths
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../../output/dsa_tokenized.pkl')
destination_path = os.path.join(script_path, '../../output/dsa_kwic_analysis.json')

# Load the tokenized text from the source file
with open(source_path, 'r', encoding='utf-8') as f:
    tokenized_text = f.read()

# Create an NLTK Text object
text = Text(tokenized_text)

# Perform KWIC analysis for the keyword
keyword = "spe"
kwic_results = list(text.concordance_list(keyword, lines=nltk.ConcordanceIndex(text.tokens).count(keyword)))

# Convert the KWIC results into JSON format
kwic_json = []
for result in kwic_results:
    kwic_json.append({
        "left_context": " ".join(result[0]),
        "keyword": result[1],
        "right_context": " ".join(result[2])
    })

# Save the KWIC analysis as a JSON file
with open(destination_path, 'w', encoding='utf-8') as f:
    json.dump(kwic_json, f, ensure_ascii=False, indent=2)

# Print a message to confirm that the file has been saved
print(f'The KWIC analysis has been saved as {destination_path}')
