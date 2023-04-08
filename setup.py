from setuptools import setup, find_packages
import os
import sys

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Install Stanza NLP models required by the scripts
if "install" in sys.argv or "develop" in sys.argv:
    os.system("python src/install/install_stanza_model.py")
    os.system("python src/install/install_fasttext_model.py")

setup(
    name="lutherscripts",
    version="0.1.0",
    description="Collection of NLP scripts to analyze your UTF-8 Latin text from a textfile",
    author="Benjam Bröijer",
    author_email="benjam.broijer@roadsign.fi",
    url="https://github.com/benjamsf/python-latinnlp-scripts",  # Replace with your repository URL if available
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Religion",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
    "console_scripts": [
        "lutherscript = lutherscripts.cli:cli_main",
        "lutherscript-gui = lutherscripts.gui:gui_main",
    ],
    },
)
)
