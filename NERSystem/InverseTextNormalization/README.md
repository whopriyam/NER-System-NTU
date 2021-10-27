
## Requirements
- Python 3.6+ (or [pyenv](https://github.com/pyenv/pyenv))
- [pipenv](https://pipenv.readthedocs.io/en/latest/) or Conda


## Installation using conda
1. Create a new conda environment using Python 3.6 (important), activate it and install the packages as follows.
```bash
conda create --name new_data_ner python=3.6
conda activate new_data_ner
conda install -c conda-forge jsonnet
conda install -c conda-forge flask
conda install -c conda-forge flask-sockets
conda install -c conda-forge pyyaml
pip install allennlp==1.1.0
pip install allennlp-models==1.1.0
python -m spacy download en_core_web_sm
pip install sentence-splitter
pip install transformers
pip install SentencePiece
pip3 install num2words
pip3 install simpletransformers
```
### Just to run the file files individually, run the command `conda install -c conda-forge thrax` to install thrax compiler.

## Grammar generation(Generation of sentence at CombineTextHighlighter\NERSystem\InverseTextNormalization\grammars )

## Run these commands to generate the sentences and perform NER
1) Navigate to /grammars/BILOU_files/covid.

2)thraxmakedep covid.grm

3)make

4)thraxrandom-generator --far=covid.far --rule=random_sentence --noutput=10000 > covid.txt

5) Run covid/fix_txt.py to generate covid_cleaned.txt (make sure before running this covid.txt should be the only txt file in the currect directory).

6) Run scripts/parser.ipynb to generate symptoms_ner.csv.

7) Go to /Transformer_NER and uncomment the corresponding model you want to use for NER.

## Run these commands to perform text augmentation
1) Once you generate the covid_cleaned.txt file, run the /Pegasus_Augmentation/Pegasus_covid.ipynb file on it and get the augmented csv file.

2) Run the remove_duplicates.ipynb file to remove duplicate augmentations and get the final output.



 
