import re
from sys import argv, exit

file = "../grammars/Covid/BILOU_files/symptoms_bilou_cleaned.txt"
outfile = "../grammars/Covid/BILOU_files/symptoms_train.bilou"

def get_tagpairs(sentence):
    sentence = sentence.strip()
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
    
    if len(words) == 0:
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

with open(file) as f:
        data = f.read()

ldata = [x for x in data.split('\n') if x]

final = []
for x in ldata:
    if x[0] != "<":
        continue
    raw_processed = sum(get_tagpairs(x), [])
    processed = [' '.join(x) for x in raw_processed]
    final.append(processed)


import pandas as pd

df = pd.DataFrame(columns = ["Sentence_Num","Word","Tag"])
c = 0
for i in range(0,len(final)):
    for item in (final[i]):
        df.at[c,"Sentence_Num"] = "Sentence: " + str(i)
        #print (item)
        temp_list = item.split(" ")
        df.at[c,"Word"] = temp_list[0]
        df.at[c,"Tag"] = temp_list[1]
        c = c+1
    #print (i)

df.to_csv("../grammars/Covid/BILOU_files/symptoms_ner.csv")