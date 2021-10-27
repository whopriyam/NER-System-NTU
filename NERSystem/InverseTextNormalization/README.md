
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
```
### Just to run the file files individually, run the command `conda install -c conda-forge thrax` to install thrax compiler.

## Grammar generation(Generation of sentence at CombineTextHighlighter\NERSystem\InverseTextNormalization\grammars )

## Run these commands to generate the sentences
1)thraxmakedep covid.grm

2)make

3)thraxrandom-generator --far=covid.far --rule=random_sentence --noutput=10000 > covid.txt

4) Run fix_txt.py to generate covid_cleaned.txt (make sure before running this covid.txt should be the only txt file in the currect directory).

5) Run parser.ipynb to generate symptoms_ner.csv.

6) Go to /Transformer_NER and uncomment the corresponding model you want to use for NER.

##Parser
Parser is to convert the sentences into a BILOU format and to clean up the file 

##training
To train with the BILOU file
1) copy the BILOU file to CombineTextHighlighter\NERSystem\InverseTextNormalization\scripts
2) put the BILOU file into the "police"Train\Train or corrosponding folder
3) run the "build_dataset.py"(this will split the ration into 8(train):1(test):1(dev)



 
