#!/usr/bin/env python3
import sys
import os

evenList = []
oddList = []

evenListFile = "even_nums.txt"
oddListFile = "odd_nums.txt"

for filename in os.listdir("/home/scitech/pegasus-workflows/Workflow3/input/"):
   with open(os.path.join("/home/scitech/pegasus-workflows/Workflow3/input/", filename), 'r') as f: # open in readonly mode
      Lines = f.readlines()
      count = 0

      for line in Lines:
          count += 1
          line = line.rstrip('\n')
          num = int(line)
          if(num%2 == 0):
              evenList.append(num)
          else:
              oddList.append(num)


print(evenList)
print(oddList)

f = open(evenListFile, "w")
for num in evenList:
    f.write(str(num)+"\n")
f.close()


f = open(oddListFile, "w")
for num in oddList:
    f.write(str(num) + "\n")
f.close()
