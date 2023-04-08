import argparse
import os
import subprocess

__author__ = "benjamsf"
__license__ = "MIT"


def add_arguments(parser):
    parser.add_argument("-o", "--operation", type=str, choices=["word_tokenize_latin", "sent_tokenize_latin"], required=True, help="Choose operation: word_tokenize_latin or sent_tokenize_latin")
    parser.add_argument("-s", "--source-path", type=str, required=True, help="The path to the source text file")
    parser.add_argument("-d", "--destination-path", type=str, required=True, help="The path to the output file")

def sentence_tokenize_latin(source_path, destination_path):
    from src.text_preparation.cltk_sentencetokenize_latin_arg import main as cltk_sentencetokenize_latin
    output = cltk_sentencetokenize_latin(source_path, destination_path)
    print(output)

def word_tokenize_latin(source_path, destination_path):
    from src.text_preparation.cltk_wordtokenize_latin_arg import main as cltk_wordtokenize_latin
    output = cltk_wordtokenize_latin(source_path, destination_path)
    print(output)

def cli_main():
    parser = argparse.ArgumentParser(description="NLP script launcher")
    add_arguments(parser)
    args = parser.parse_args()

    source_path = os.path.abspath(args.source_path)
    destination_path = os.path.abspath(args.destination_path)

    if args.operation == 'sent_tokenize_latin':
        sentence_tokenize_latin(source_path, destination_path)
    elif args.operation == 'word_tokenize_latin':
        word_tokenize_latin(source_path, destination_path)

if __name__ == '__main__':
    cli_main()


