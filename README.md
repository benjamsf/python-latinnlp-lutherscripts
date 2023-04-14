# Luther Scripts
## A Latin NLP project
MIT-License, (c) Benjam Bröijer (u:benjamsf)

## What
A Python suite to perform Natural Language Processing (NLP), on a Latin source text supplied by the user. Support included for source text from Luther's Werke im WWW, a Weimarer Ausgabe -rendition offered by ProQuest, LLC, but you could use these for any Latin text you specifically provide yourself in UTF-8 .txt-files.

## Why
I noticed that while the tools to do the actual hard work are present and available, I found no ready scripts to do the kind of a trivial work to tokenize and analyze a Latin text that is not from eg. LatinCorpus by CLTK itself. So I made these for my thesis work, and made them public in case anybody else needs to do similar tasks. 

## How
I update the documentation as I grow the tools. I intend to make this library easy to install and use.

## As per development version 0.3.0

## Features
### From the CLI:

**Word tokenization**, including:
- - Lemmatization
- - Stopword filtering
- - Reading and storing, if supplied, metadata from the source text file, metadata form: #metadata,as,much,here,as,you,want# document #end# #next,document,metadata# document2 #end#, to the word tokenized file

**Example cli command:**
lutherscripts-cli -o word_tokenize_latin -s lutherscripts/txt/your_input.txt -d lutherscripts/output/your_wordtokenized.json

**Corpus builder**, including:
- - Building a dictionary saved to a Pickle, and a corpus saved to a MatrixMarket file, from a word tokenized json file

**Topic modeler**, including:
- - Parameters: Number of topics to be generated, Number of passes on the corpus to find the topics, Number of iterations of the automated hyperparameter function, Source word tokenized file, Source corpus file, Source dictionary file
- - Automatic hyperparameter tuning processes (Random Search method implemented)
- - Topics generetion
- - Topic distribution
- - Document topic distribution
- - Word topic distribution
- - Coherence score

**Example cli command:**
lutherscripts-cli -o topic_modeling -1 3 -2 30 -3 100 -s lutherscripts/txt/your_wordtokenized.json -c lutherscripts/output/your_input_corpus.mm -dc lutherscripts/output/your_input_dictionary.pkl -d lutherscripts/output/your_intended_output_results.json

**From GUI:**
- Word tokenization
- Corpus builder
- Implement the rest once the actual functions are mature enough, so that I don't need to mess with the gui code repeatedly
- Luther's eyes reading a book when an operation is running

### Operation instructions
1. install via pip install python-latinnlp-lutherscripts/
2a. In Windows, navigate powershell to the main directory and run 'run_lutherscripts.bat' for GUI
2b. In linux, run 'lutherscripts' for GUI
3. CLI: lutherscripts-cli -o word_tokenize_latin/sent_tokenize_latin -s (source file relative path) -d (destination file relative path)

### TODO:
- Call Luther's Werke im WWW -related text preparation functions from cli and gui
- Make KWIC and FreqAn work from both cli and gui
- Call couple of else NLP tools from cli and gui
