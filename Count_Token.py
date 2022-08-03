#this program tokenizes the texts and returns the number of tokens of the corpus
#author: Lisa Kiss
#start date: 03.08.22

import os
import numpy as np
from pprint import pprint

files= os.listdir(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Nur_txt')
wordlist = []
for file in files:
    path = os.path.join(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Nur_txt', file)
    opened = open(path, encoding="utf-8")
    content = opened.read()
    wordlist.append(content.split())
tokencount = 0
count_list = []
for item in wordlist:
    count_list.append(len(item)-700) #to calculate the average and the standard deviation
    tokencount = tokencount + len(item)
print(tokencount)

#Average
average = sum(count_list) / len(count_list)
print(sum(count_list))
print (average)

#Standard deviation
print (np.std(count_list))
