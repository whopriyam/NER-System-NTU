export NER_TRAIN_PATH=policeTrain/Police/train.bilou
export NER_VAL_PATH=policeTrain/Police/dev.bilou
export OUTPUT=models_Police/ner_experiment

allennlp train ner_config/ner_elmo.jsonnet -s $OUTPUT --include-package addresses_ner
