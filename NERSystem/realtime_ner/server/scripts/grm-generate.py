import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description='Generate N non-repeating sentences from the grammer.')
parser.add_argument('--N', action="store", dest="outputs", type=int, default=1000000)
noutputs = parser.parse_args().outputs

output = os.popen('thraxrandom-generator --far=modifiedgrammar-v4.far --rule=COMMANDS --noutput='+str(noutputs)).read()
lines = output.split("\n")

file = open("sentences-generated-grm.txt", "w")
for i in range(noutputs):
	file.write(lines[3*i+1].strip()+'\n')
	if (i%1000000 == 0):
		file.close()
		file = open("sentences-generated-grm.txt", "a")
file.close()
