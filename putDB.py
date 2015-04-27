import json
import pymongo
from pymongo import MongoClient

def connect():
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client['Tweets']
	return client,db

if __name__ == "__main__":
	client, db = connect()
	infile = open("data.csv","r")
	data = json.load(infile)

	print "Got Tweets, putting in mongodb" 
	
	for item in data:
		tweets = db.tweets.insert(item)
		
	print "Done  putting in mongodb" 
