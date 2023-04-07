import io
import os
import re
from cltk import NLP
from tqdm import tqdm
import logging

def main(source_path, destination_path):
    # Instantiate a Latin-specific NLP object
    logging.basicConfig(level=logging.ERROR)
    cltk_nlp = NLP(language="lat")

    # Load the Latin text from the source file
    input_file = os.path.abspath(source_path)
    with open(input_file, 'r', encoding='utf-8') as f:
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

    # Capture the output in a string buffer
    with io.StringIO() as buffer:
        for chunk in tqdm(text_chunks, desc="Tokenizing sentences"):
            doc = cltk_nlp(chunk)
            for sentence in doc.sentences:
                sentence_text = ' '.join([word.string for word in sentence.words])
                sentence_tokens.append(sentence_text.strip())

        buffer.write('\n'.join(sentence_tokens))

        # Save the tokenized output to a file
        output_file = os.path.abspath(destination_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(buffer.getvalue())

        # Print a message to confirm that the file has been saved
        print(f'The tokenized output has been saved as {destination_path}')

    # Return the output as a string
    return buffer.getvalue()


