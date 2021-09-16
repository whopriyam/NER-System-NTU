import os
import num2words
import re


path  = os.path.dirname(os.path.abspath(__file__))
fileName = ""


num_list = ["one","two","three","four","five","six","seven","eight","nine"]

for file in os.listdir(path):
    if file.endswith(".txt") and file[0]!=".":
        fileName = file


crimefile = open(path+"/"+fileName, 'r')
yourResult = [line.split('\n') for line in crimefile.readlines()]
#print (yourResult)

inList = []
c = 0

for item in yourResult:
	c = c+1
	if c==4:
		c = 1
	if c%2==0:
		item[0] = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), item[0])
		item[0] = item[0].lower()
		# print (item[0])
		item[0] = list((item[0]).split(" "))
		# print (item)

		tlist = []
		for i in range(0,len(item[0])):

			try:
				if (item[0])[i] == "zero" and (item[0])[i-1] not in num_list:
					tlist.append("")
				else:
					tlist.append((item[0])[i])
			except:
				if (item[0])[i] == "zero":
					tlist.append("")
				else:
					tlist.append((item[0])[i])



		#inList.append(item[0])
		inList.append(" ".join((" ".join(tlist)).split()))
		#inList.append(" ".join(tlist))


inList2 = [i for i in inList if i != "****************************************"]
inList2 = list(set(inList2))


with open(path+"/"+fileName[:-4]+"_cleaned.txt", 'w') as output:
    for row in inList2:
        output.write(str(row) + '\n')