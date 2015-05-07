import csv
from collections import defaultdict

def get_data_from_file(filename):
    csvfile = open(filename,"r")
    data = csv.reader(csvfile)
    fieldNames = data.next()
    print fieldNames
    results = defaultdict()
    i = 0
    for item in data:
        print item[1].decode('unicode_escape').encode('ascii','ignore')
        results[i] = {fieldNames[0]:i, fieldNames[1]:item[1], fieldNames[2]:item[2], fieldNames[3]:item[3] }
        i+=1
    csvfile.close()
    print len(results)

if __name__ == "__main__":
    inputFile = "Train.csv"
    get_data_from_file(inputFile)
