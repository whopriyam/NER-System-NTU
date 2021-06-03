from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor
from allennlp_models.tagging.models.crf_tagger import CrfTagger
from addresses_ner.predictors.itn_entity_tagger import ItnEntityTaggerPredictor
import allennlp_models
from spacy.tokens import Token, Doc, Span
import yaml

# import itn_model

valid_tags = ["Addr-Building-Number","Addr-Block" , "Addr-Bld", "Addr-Street", "PostCode", "Addr-Region","Addr-Building-Name", "Addr-UnitNo", "Addr-city", "AGE", "INJURY", "Addr-Block", "IC", "COUNT", "BODYLOCATION", "STATUS", "CONDITION" ]

with open("config.yaml") as configfile:
    config = yaml.load(configfile)
    ner_model_archive = config["model_archive_path"]["ner"]


class ItnEntityTagger(object):
    """
    Spacy pipeline component for ITN Entities tagger
    """

    name = "ITN Entity Tagger"

    def __init__(self, nlp):
        archive = load_archive(ner_model_archive)
        self.predictor = Predictor.from_archive(
            archive, predictor_name="itn-entity-tagger")

        Token.set_extension("itn_ent_bilou_", default="")
        Token.set_extension("itn_ent_type_", default="")
        Token.set_extension("itn_ent_type", default=0)
        Doc.set_extension("itn_ents", default=())

        for tag in valid_tags:
            nlp.vocab.strings.add(tag)
        self.vocab = nlp.vocab

    def __call__(self, doc):
        self.set_itn_ent(doc)
        self.create_itn_ent_span(doc)

        return doc

    def set_itn_ent(self, doc):
        prediction = self.predictor.predict(tokens=doc)
        tags = prediction["tags"]
        
        print(tags)
        for i, tag in enumerate(tags):
            split_tag = tag.split("-")
            bilou = split_tag[0]
            ent_type_ = ""
            ent_type = 0

            if len(split_tag) >= 2:
                ent_type_ = '-'.join(split_tag[1:])
                ent_type = self.vocab.strings[ent_type_]

            doc[i]._.set("itn_ent_bilou_", bilou)
            doc[i]._.set("itn_ent_type_", ent_type_)
            doc[i]._.set("itn_ent_type", ent_type)

    def create_itn_ent_span(self, doc):
        ent_spans = []
        b_idx = 0

        for i, token in enumerate(doc):
            label = self.vocab.strings[token._.itn_ent_type_]

            if token._.itn_ent_bilou_ == "U":
                ent_spans.append(Span(doc, i, i + 1, label=label))
            elif token._.itn_ent_bilou_ == "B":
                b_idx = i
            elif token._.itn_ent_bilou_ == "L":
                ent_spans.append(Span(doc, b_idx, i + 1, label=label))

        doc._.set("itn_ents", tuple(ent_spans))
