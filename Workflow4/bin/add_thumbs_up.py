#!/usr/bin/env python3
import sys
import emojis
import argparse

parser = argparse.ArgumentParser("parser for input and output file")
parser.add_argument('-I', '--input', required=True, metavar = '', help='input file')
parser.add_argument('-O', '--output', required=True, metavar='', help='output file')

args = parser.parse_args()

inputFilePath = args.input
outputFileName = args.output
   
print(inputFilePath)
print(outputFileName)

message = ""
with open(inputFilePath) as f:
    message = f.readline()
    message = message + emojis.encode(':thumbs_up:')

print("Here in code")
f = open(outputFileName, "w")
f.write(message)
f.close()



