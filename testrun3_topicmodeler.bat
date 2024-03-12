@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o topic_modeling -1 10 -2 100 -3 5 -s python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_march24_1.json -c python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_mar24_corpustest.json_corpus.mm -dc python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_mar24_corpustest.json_dictionary.pkl -d python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_topictest.json
