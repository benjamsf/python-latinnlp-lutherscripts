import argparse
import os
import subprocess

def add_arguments_sentencetokenize(parser):
    parser.add_argument("-s", "--source-path", type=str, required=True, help="The path to the source text file")
    parser.add_argument("-d", "--destination-path", type=str, required=True, help="The path to the output file")

def add_arguments_wordtokenize(parser):
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


def main():
    parser = argparse.ArgumentParser(description="NLP script launcher")

    subparsers = parser.add_subparsers(dest='subparser_name')

    sent_tokenize_parser = subparsers.add_parser('sent_tokenize_latin', help='Tokenize Latin text into sentences')
    add_arguments_sentencetokenize(sent_tokenize_parser)

    word_tokenize_parser = subparsers.add_parser('word_tokenize_latin', help='Tokenize Latin text into words')
    add_arguments_wordtokenize(word_tokenize_parser)

    args = parser.parse_args()

    if args.subparser_name == 'sent_tokenize_latin':
        sentence_tokenize_latin(args.source_path, args.destination_path)
    elif args.subparser_name == 'word_tokenize_latin':
        word_tokenize_latin(args.source_path, args.destination_path)

    return args

if __name__ == '__main__':
    args = main()
    if args.subparser_name == 'word_tokenize_latin':
        word_tokenize_latin(args.source_path, args.destination_path)
    elif args.subparser_name == 'sent_tokenize_latin':
        sentence_tokenize_latin(args.source_path, args.destination_path)

        print(output)