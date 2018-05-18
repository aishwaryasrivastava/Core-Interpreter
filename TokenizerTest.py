from Tokenizer import Tokenizer
from TokenKind import TokenKind
from enum import Enum
import sys

# Test driver for Part 2 for CSE 3341 Core Interpreter project.
# Author:	Aishwarya Srivastava
# Date:		03/03/2018

# Reading the file and creating a list of words
filename = sys.argv[1]
infile = open(filename, "r")

tail = []
for line in infile:
	for string in line.split():
		tail.append(string)
infile.close()

# Opening output file for writing
nameAndFormat = filename.split(".txt")
outfilename = "testoutput.txt".join(nameAndFormat)
outfile = open(outfilename, "w")

# Creating a tokenizer
t = Tokenizer(tail)
while t.getToken() != TokenKind.EOF and t.getToken() != TokenKind.ERROR:
	print(str(t.getToken().value)+"\n")
	t.skipToken()

if (t.getToken() == TokenKind.EOF):
	print(str(t.getToken().value)) 
else:
	print("ERROR! Invalid token \"" + t.getTokenName() + "\"!")

outfile.close()