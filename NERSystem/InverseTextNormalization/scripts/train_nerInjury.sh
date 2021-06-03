export NER_TRAIN_PATH=injuriesTrain/injuries/train.bilou
export NER_VAL_PATH=injuriesTrain/injuries/dev.bilou
export OUTPUT=model_Injury/ner_experiment

allennlp train ner_config/ner_elmo.jsonnet -s $OUTPUT --include-package addresses_ner
