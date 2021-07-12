
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

2. Download the NER model archive [here] (https://drive.google.com/drive/folders/1fM7vtmU1XExBl7tv1D_4ZUj0SJL9cmyH?usp=sharing), and copy it to `models/` directory. Optionally, if you use your own NER model, modify the archived model path in `config.yaml`

## Starting the server at (CombineTextHighlighter\NERSystem\InverseTextNormalization\realtime_server\emergencyCallServer(5001))

## The port number is written at the end of the sever name
conda activate new_data_ner

To start the server
```bash
$ ./run_server.py --port 5001
```

##starting the frount end at (CombineTextHighlighter\NERSystem\realtime_ner\frontend)
npm run dev

## API
Currently, you make an API call to the server only via WebSocket. Simply establish connection to the server's root URL (`/`), and then send the text in string directly on the message.

Example in JavaScript:
```js
// First, create a websocket connection
const ws = new WebSocket("ws://localhost:5000/");
// Pass callback function to `onmessage` when receive message from server
ws.onmessage = (e) => {
    console.log(e.data);
}
// Using `send` method, send message to server
ws.send("singapore one two cleared for takeoff");
```

### Just to run the file files individually, run the command `conda install -c conda-forge thrax` to install thrax compiler.

## Grammar generation(Generation of sentence at CombineTextHighlighter\NERSystem\InverseTextNormalization\grammars )

## Run these commands to generate the sentences
1)thraxmakedep police.grm

2)make

3)thraxrandom-generator --far=domain.far --rule=random_sentence --noutput = 1000000 > emergencysen.txt

##itn_entity_tagger.py
this contains the spacy pipeline component(adds all the valid tags)

##Web socket ENDPOINTS
CombineTextHighligher\NERSystem\realtime_ner\frountend\data.json
This file contains the list of examples and the NER websocket end points new end points can be simply add here.

##Parser
CombineTextHighlighter\NERSystem\InverseTextNormalization\grammars
Parser is to convert the sentences into a BILOU format and to clean up the file 

##trainning
To train with the BILOU file
1) copy the BILOU file to CombineTextHighlighter\NERSystem\InverseTextNormalization\scripts
2) put the BILOU file into the "police"Train\Train or corrosponding folder
3) run the "build_dataset.py"(this will split the ration into 8(train):1(test):1(dev)
4) delete any models
5) conda activate new_data_ner
6) run the command "sh train_nerInjury.sh
7) after the train finish copy "models_Police\ner_experiment\model.tar.gz" to
"CombineTextHighlighter\NERSystem\InverseTextNormalization\realtime_server\police(5003)\models"




 
