# Python script to prepare Luther's Werke im WWW text to form usable in NLP
# Removes any square brackets [] and their contents, except for page and verse numbers 

__author__ = "benjamsf"
__license__ = "MIT"

import os
import re

# Define the source and destination file names and paths
# Target text to projectfolder/txt/target_txt
# Output text to projectfolder/txt/output_txt
script_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_path, '../txt/dsa.txt')
destination_path = os.path.join(script_path, '../output/dsa_modified.txt')

# Load the text from the source file
with open(source_filename, 'r', encoding='utf-8') as f:
    sourcetext = f.read()

# Define a function to process matches in re.sub
def process_match(match):
    if re.match(r'\[(Seite \d+|\d+)\]', match.group(0)):
        return match.group(0)
    else:
        return ''

# Remove square brackets and their content (except for page and verse numbers)
sourcetext = re.sub('\[[^\]]*?\]', process_match, sourcetext)

# Remove WA notes from the text
sourcetext = re.sub('Anmerkung ansehen \/ view note', '', sourcetext)

# Preprocess the text by removing newlines and extra whitespace
sourcetext = re.sub('\n+', ' ', sourcetext)
sourcetext = re.sub('\s+', ' ', sourcetext)

# Save the modified text to the destination file
with open(destination_filename, 'w', encoding='utf-8') as f:
    f.write(sourcetext)

# Print a message to confirm that the file has been saved
print(f'The modified text has been saved as {destination_filename}')
