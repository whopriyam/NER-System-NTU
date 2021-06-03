import json
from collections import Counter

with open("server/utils/numbers.en.json") as numbers_file:
    numbers_dict = json.loads(numbers_file.read())


def _prefix_with_zero(tokens):
    """
    Prefix `tokens` from `words_to_numbers` with zero if
    first token is zero
    """
    if tokens[0] in numbers_dict["decimal"]:
        return ["zero"] + tokens
    return tokens


def _words_to_digits(tokens):
    """
    Take tokens and return a digit token in a list
    """
    decimal_tokens = []
    word_count = Counter(tokens)
    digits = []
    decimal_digits = []

    # ensure that there's only one decimal
    decimal_count = 0
    for decimal_word in numbers_dict["decimal"]:
        decimal_count += word_count[decimal_word]
    if decimal_count > 1:
        return tokens

    # prefix with zero if needed
    tokens = _prefix_with_zero(tokens)

    # split words to 2 list if decimal is present
    if decimal_count == 1:
        cur_list = new_tokens = []
        for word in tokens:
            if word in numbers_dict["decimal"]:
                cur_list = decimal_tokens
                continue
            cur_list.append(word)

        if not decimal_tokens:
            return tokens

        tokens = new_tokens

    # parsing it right to left here
    prev_is_base = False
    for token in tokens[::-1]:
        if token in numbers_dict["base"]:
            digits.append(numbers_dict["base"][token])
            prev_is_base = True
        elif token in numbers_dict["tens"]:
            digits.extend(list(numbers_dict["tens"][token])[::-1])
            prev_is_base = False
        elif token in numbers_dict["tensExtendable"]:
            if prev_is_base:
                digits.append(numbers_dict["tensExtendable"][token][0])
            else:
                digits.extend(
                    list(numbers_dict["tensExtendable"][token])[::-1])
            prev_is_base = False
        elif token in numbers_dict["units"]:
            zero_count = numbers_dict["units"][token]
            if len(digits) > zero_count:
                # invalid usage of units e.g. hundred & thousand
                return tokens
            digits.extend(["0" for _ in range(zero_count - len(digits))])
            prev_is_base = False
        else:
            # if the number is not 'clean' dont convert it
            return tokens

    if decimal_tokens:
        decimal_digits.append(".")
        for word in decimal_tokens:
            if word in numbers_dict["base"]:
                decimal_digits.append(numbers_dict["base"][word])
            else:
                # if the number is not 'clean' dont convert it
                return tokens

    return ["".join(digits[::-1]) + "".join(decimal_digits)]


def _token_is_in_dict(token):
    return (token in numbers_dict["base"] or token in numbers_dict["decimal"]
            or token in numbers_dict["units"] or token in numbers_dict["tens"]
            or token in numbers_dict["tensExtendable"])


def _cluster_tokens_to_spans(tokens):
    """
    Take tokens and return list of tokens clustered if the continous
    span is numbers or not
    """
    spans = []
    span = {"is_numbers": False, "tokens": []}
    prev_is_numbers = False

    for token in tokens:
        if _token_is_in_dict(token):
            if not prev_is_numbers:
                spans.append(span)
                span = {"is_numbers": True, "tokens": []}
            span["tokens"].append(token)
            prev_is_numbers = True
        else:
            if prev_is_numbers:
                spans.append(span)
                span = {"is_numbers": False, "tokens": []}
            span["tokens"].append(token)
            prev_is_numbers = False

    spans.append(span)

    return spans


def replace_words_with_digits(text):
    """
    Take a string `text` and return a new `text` with the numbers in words
    replaced with digits
    """
    # do a simple split for tokenization
    tokens = text.split()

    spans = _cluster_tokens_to_spans(tokens)

    replaced_tokens = []

    for span in spans:
        if span["is_numbers"]:
            replaced_tokens.extend(_words_to_digits(span["tokens"]))
        else:
            replaced_tokens.extend(span["tokens"])

    return " ".join(replaced_tokens)
