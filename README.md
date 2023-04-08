# Luther Scripts
## A Latin NLP project
MIT-License, (c) Benjam Bröijer (u:benjamsf)

## What
Collection of Python scripts to perform Natural Language Processing (NLP) on Latin source text supplied by the user. Support for source text from Luther's Werke im WWW, a Weimarer Ausgabe -rendition offered by ProQuest, LLC, but you could use these for any Latin text you specifically provide yourself in UTF-8 .txt-files.

## Why
I noticed that while the tools to do the actual hard work are present and available, I found no ready scripts to do the kind of a trivial work to tokenize and analyze a Latin text that is not from eg. LatinCorpus by CLTK itself. So I made these for my thesis work, and made them public in case anybody else needs to do similar tasks. 

## How
I update the documentation as I grow the tools. By now there are capabilities to prepare text from Luther's Werke im WWW, and to tokenize words. I intend to make this library easy to install and use.

## As per development version 0.2.0

### Features
- Word tokenization from Latin source text
- Sentence tokenization from Latin source text
- Working CLI, working but WIP GUI

### Operation instructions
1. install via pip install python-latinnlp-lutherscripts/
2a. In Windows, navigate powershell to the main directory and run 'run_lutherscripts.bat'
2b. In linux, run 'lutherscripts'
3. CLI: lutherscripts-cli -o word_tokenize_latin/sent_tokenize_latin -s (source file relative path) -d (destination file relative path)

### TODO:
- Call Luther's Werke im WWW -related text preparation functions from cli and gui
- Call Keyword in Context (KWIC) analysis from cli and gui
- Call couple of else NLP tools from cli and gui
- Make gui look sane and usable
