from spacy.tokens import Token
from spacy.matcher import Matcher

AIRLINE_DESIGNATORS = [["SINGAPORE"], ["JET", "STAR", "ASIA"]]


def create_call_sign_patterns():
    patterns = []
    for designator in AIRLINE_DESIGNATORS:
        unit_pattern = []
        for token in designator:
            unit_pattern.append({'LOWER': token.lower()})
        for _ in range(4):
            unit_pattern.append({'LIKE_NUM': True, 'OP': '?'})
        patterns.append(unit_pattern)

    return patterns


class BasicAtc(object):
    def __init__(self, nlp):
        call_sign_patterns = create_call_sign_patterns()
        Token.set_extension('call_sign', default=False)
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('CallSign', None, *call_sign_patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            # if match_id == 'CallSign':
            spans.append(doc[start:end])
        for span in spans:
            span.merge()
            for token in span:
                token._.call_sign = True

        return doc