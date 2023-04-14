@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o topic_modeling -1 3 -2 30 -3 100 -s lutherscripts/txt/jalla.json -c lutherscripts/output/DSAkoe_corpus.mm -dc lutherscripts/output/DSAkoe_dictionary.pkl -d lutherscripts/output/DSA_topictest.json
