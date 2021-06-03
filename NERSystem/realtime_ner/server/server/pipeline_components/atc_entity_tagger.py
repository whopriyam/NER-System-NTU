from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor
from spacy.tokens import Token, Doc, Span
import yaml

import atc_model

valid_tags = ["BUILDINGNUM", "CITY", "UNITNO", "POSTCODE", "BUILDINGNAME", "BLOCK", "STREET","OTHERS","NUMBER"]

with open("config.yaml") as configfile:
    config = yaml.safe_load(configfile)
    ner_model_archive = config["model_archive_path"]["ner"]


class AtcEntityTagger(object):
    """
    Spacy pipeline component for ATC Entities tagger
    """

    name = "ATC Entity Tagger"

    def __init__(self, nlp):
        archive = load_archive(ner_model_archive)
        self.predictor = Predictor.from_archive(
            archive, predictor_name="atc-entity-tagger")

        Token.set_extension("atc_ent_bilou_", default="")
        Token.set_extension("atc_ent_type_", default="")
        Token.set_extension("atc_ent_type", default=0)
        Doc.set_extension("atc_ents", default=())

        for tag in valid_tags:
            nlp.vocab.strings.add(tag)
        self.vocab = nlp.vocab

    def __call__(self, doc):
        self.set_atc_ent(doc)
        self.create_atc_ent_span(doc)

        return doc

    def set_atc_ent(self, doc):
        prediction = self.predictor.predict(tokens=doc)
        tags = prediction["tags"]
        print(tags)
        for i, tag in enumerate(tags):
            split_tag = tag.split("-")
            bilou = split_tag[0]
            ent_type_ = ""
            ent_type = 0

            if len(split_tag) == 2:
                ent_type_ = split_tag[1]
                ent_type = self.vocab.strings[ent_type_]

            doc[i]._.set("atc_ent_bilou_", bilou)
            doc[i]._.set("atc_ent_type_", ent_type_)
            doc[i]._.set("atc_ent_type", ent_type)

    def create_atc_ent_span(self, doc):
        ent_spans = []
        b_idx = 0

        for i, token in enumerate(doc):
            print(token._.atc_ent_type_)
            label = self.vocab.strings[token._.atc_ent_type_]

            if token._.atc_ent_bilou_ == "U":
                ent_spans.append(Span(doc, i, i + 1, label=label))
            elif token._.atc_ent_bilou_ == "B":
                b_idx = i
            elif token._.atc_ent_bilou_ == "L":
                ent_spans.append(Span(doc, b_idx, i + 1, label=label))

        doc._.set("atc_ents", tuple(ent_spans))
