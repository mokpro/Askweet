import csv
import json
from collections import defaultdict

if __name__ == "__main__":
    infile1 = open("lexical_tags.json","r")
    infile2 = open("wordnet_tags.json","r")
    infile3 = open("postags.json","r")
    data1 = json.load(infile1)
    data2 = json.load(infile2)
    data3 = json.load(infile3)

    print len(data1),len(data2),len(data3)

    for item in data2:
        data1[item].extend(data2[item])

    for item in data3:
        data[item].extend(data[item])
