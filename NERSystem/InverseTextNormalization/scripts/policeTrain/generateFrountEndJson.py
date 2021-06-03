import random
import json

def count_capital_words(filename):                                               
    count = 0
    originalList=[]
    noRepeat=[]
    with open(filename, 'r') as fp:
        
        for line in fp:                                                          
            for word in filter(None, line.split()):                              
                if (word[0].isupper()and len(word)>1):                                            
                    count += 1
                    word=word[2:]
                   # print(word)
                    originalList.append(word)
        [noRepeat.append(x) for x in originalList if x not in noRepeat]
    return noRepeat

def generateRandomColor():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    #print('A  Random Hex Color Code is :',hex_number)
    return hex_number

def generateJsonWithColor(Alist):
    dicts = {}
    for x in Alist:
        dicts[x] = generateRandomColor()
    y = json.dumps(dicts)
    return y
def writeJson(y):
    f = open("highlight.txt", "x")
    f.write(y)
    f.close()
def main():
    filename='test.BILOU'
    s=generateJsonWithColor(count_capital_words(filename))
    writeJson(s)
    print(s)  # 8
    
main()
