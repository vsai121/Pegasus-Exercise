#!/usr/bin/env python3
import sys
import emojis

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])

print("\nArguments passed:", end = " ")
for i in range(1, n):
   print(sys.argv[i], end = " ")
   
print('\n')
inputFilePath = sys.argv[1]
outputFileName = sys.argv[2]
   
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



