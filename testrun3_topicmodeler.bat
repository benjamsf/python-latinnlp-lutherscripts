@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o topic_modeling -1 2 -2 100000 -s lutherscripts/txt/habibicorpus_corpus.mm -dc lutherscripts/txt/habibicorpus_dictionary.pkl -d lutherscripts/txt/topictest.json
