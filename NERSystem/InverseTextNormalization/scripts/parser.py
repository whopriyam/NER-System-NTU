#! /usr/bin/python3

import re
from sys import argv, exit


def get_tagpairs(sentence):
    wordlist = re.split(r'(?<=>)(.+?)(?=<)', sentence)
    raw_taglist = wordlist[::4]

    taglist = [x[1:-1] for x in raw_taglist]

    phrases = map(str.strip, wordlist[1::4])
    tagged = map(lambda x: tag_items(x[0], x[1]), zip(taglist, phrases))

    return tagged


def tag_items(tag, phrase):
    HEADER = 'B-{}'.format(tag)
    TRAILER = 'L-{}'.format(tag)
    MIDDLE = 'I-{}'.format(tag)
    SINGLE = 'U-{}'.format(tag)

    words = [x.lower() for x in phrase.split()]

    if tag == 'O':
        return [[x, 'O'] for x in words]

    if len(words) == 1:
        return [[words[0], SINGLE], ]

    if len(words) == 2:
        return [[words[0], HEADER], [words[1], TRAILER]]

    intermediaries = [[x, MIDDLE] for x in words[1:-1]]

    result = []
    result.extend([[words[0], HEADER], ])
    result.extend(intermediaries)
    result.extend([[words[-1], TRAILER], ])

    return result


try:
    with open(argv[1]) as f:
        data = f.read()
except IndexError:
    print('Usage: {} <input file>'.format(argv[0]))
    exit(-1)

ldata = [x for x in data.split('\n') if x]

final = []
for x in ldata:
    raw_processed = sum(get_tagpairs(x), [])
    processed = [' '.join(x) for x in raw_processed]
    final.append(processed)

DELIMITER = '\n\n-DOCSTART- O\n\n'
final = ['\n'.join(x) for x in final]

final_output = DELIMITER[2:] + DELIMITER.join(final) + '\n'

with open(argv[1].split('.')[0] + '.bilou', 'w') as f:
    f.write(final_output)
