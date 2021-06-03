import spacy

from scripts.pipeline_components.itn_entity_tagger import ItnEntityTagger

nlp = spacy.load("en_core_web_sm")
nlp.remove_pipe("ner")
nlp.add_pipe(ItnEntityTagger(nlp), last=True)


def annotate(text=""):
    if not text:
        return ""
    text = text.lower()
    doc = nlp(text)

    markup = _create_entities_markup(doc)

    return markup


def _create_entities_markup(doc):
    markup_tokens = []

    for token in doc:
        bilou = token._.itn_ent_bilou_
        type_ = token._.itn_ent_type_

        if bilou == "U":
            markup_tokens.extend([f"<{type_}>", token.text, f"</{type_}>"])
        elif bilou == "B":
            markup_tokens.extend([f"<{type_}>", token.text])
        elif bilou == "L":
            markup_tokens.extend([token.text, f"</{type_}>"])
        else:
            markup_tokens.append(token.text)

    return " ".join(markup_tokens)