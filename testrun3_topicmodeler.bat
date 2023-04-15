@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o topic_modeling -1 3 -2 100 -3 50 -s lutherscripts/output/dsa_tokenized.json -c lutherscripts/output/DSACorpus1_corpus.mm -dc lutherscripts/output/DSACorpus1_dictionary.pkl -d lutherscripts/output/DSACorpus1_topictest.json
