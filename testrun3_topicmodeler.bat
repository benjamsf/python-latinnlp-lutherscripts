@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o topic_modeling -1 6 -2 10 -s lutherscripts/output/DSA_tokenized.json_corpus.mm -dc lutherscripts/output/DSA_tokenized.json_dictionary.pkl -d lutherscripts/output/DSA_topictest.json
