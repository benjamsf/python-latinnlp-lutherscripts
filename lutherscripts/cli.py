import argparse
import os
import subprocess
import sys
from pathlib import Path

__author__ = "benjamsf"
__license__ = "MIT"

# Add the parent directory of this file to the system path
file_path = Path(__file__).resolve()
sys.path.append(str(file_path.parent))


def add_arguments(parser):
    parser.add_argument("-o", "--operation", type=str, choices=["word_tokenize_latin", "sent_tokenize_latin", "kwic_analysis", "freq_analysis"], required=True, help="Choose operation: word_tokenize_latin, sent_tokenize_latin, or kwic")
    parser.add_argument("-1", "--first-detail", type=str, help="First detail flag for operation, depends on the operation")
    parser.add_argument("-2", "--second-detail", type=int, help="Second detail flag for operation, depends on the operation")
    parser.add_argument("-s", "--source-path", type=str, required=True, help="The path to the source text file")
    parser.add_argument("-d", "--destination-path", type=str, required=True, help="The path to the output file")

def sentence_tokenize_latin(source_path, destination_path):
    from src.text_preparation.cltk_sentencetokenize_latin_arg import main as cltk_sentencetokenize_latin
    output = cltk_sentencetokenize_latin(source_path, destination_path)
    print(output.encode('utf-8'))

def word_tokenize_latin(source_path, destination_path):
    from src.text_preparation.cltk_wordtokenize_latin_arg import main as cltk_wordtokenize_latin
    output = cltk_wordtokenize_latin(source_path, destination_path)
    print(output.encode('utf-8'))

def kwic_analysis(keyword, context_size, source_path, destination_path):
    from src.text_processing.nltk_do_kwic import main as nltk_do_kwic_analysis
    output = nltk_do_kwic_analysis(keyword, context_size, source_path, destination_path)
    print(output.encode('utf-8'))

def freq_analysis(source_path, destination_path):
    from src.text_processing.nltk_do_freqanalysis import main as nltk_do_freqanalysis
    output = nltk_do_freqanalysis(source_path, destination_path)
    print(output.encode('utf-8'))

def cli_main():
    parser = argparse.ArgumentParser(description="Lutherscript operations launcher")
    add_arguments(parser)
    args = parser.parse_args()

    source_path = os.path.abspath(args.source_path)
    destination_path = os.path.abspath(args.destination_path)

    if args.operation == 'sent_tokenize_latin':
        sentence_tokenize_latin(source_path, destination_path)
    elif args.operation == 'word_tokenize_latin':
        word_tokenize_latin(source_path, destination_path)
    elif args.operation == 'kwic':
        if not args.first_detail or not args.second_detail:
            print("Both -1 and -2 flags must be provided for the KWIC operation.")
        else:
            kwic_analysis(args.first_detail, args.second_detail, source_path, destination_path)
    elif args.operation == 'freq-analysis':
        freq_analysis(source_path, destination_path)

if __name__ == '__main__':
    cli_main()


