@echo off
set PYTHONIOENCODING=utf-8
set "PYTHON_SCRIPTS_PATH=C:\Users\bg1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
set "PATH=%PYTHON_SCRIPTS_PATH%;%PATH%"
lutherscripts-cli -o build_corpus -s python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_march24_1.json -d python-deservoarbitrio-textanalysis/lutherscripts/output/dsa_mar24_corpustest
