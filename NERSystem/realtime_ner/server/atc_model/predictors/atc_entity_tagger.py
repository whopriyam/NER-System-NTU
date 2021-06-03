from overrides import overrides
from typing import List

from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.models import Model
from allennlp.predictors.predictor import Predictor
from spacy.tokens import Token


@Predictor.register("atc-entity-tagger")
class AtcEntityTaggerPredictor(Predictor):
    """
    Predictor for any model that takes in a list of tokens and returns
    a single set of tags for it. Does not implement JSON methods.
    In particular, it can be used with the
    :class:`~allennlp.models.crf_tagger.CrfTagger` model
    """

    def __init__(self, model: Model, dataset_reader: DatasetReader) -> None:
        super().__init__(model, dataset_reader)

    def predict(self, tokens: List[Token]) -> JsonDict:
        instance = self._dataset_reader.text_to_instance(tokens)
        return self.predict_instance(instance)

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        raise NotImplementedError

    @overrides
    def predict_batch_json(self, inputs: List[JsonDict]) -> List[JsonDict]:
        raise NotImplementedError

    @overrides
    def predict_batch_instance(self,
                               instances: List[Instance]) -> List[JsonDict]:
        raise NotImplementedError

    def _batch_json_to_instances(self,
                                 json_dicts: List[JsonDict]) -> List[Instance]:
        raise NotImplementedError