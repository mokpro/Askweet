import json
import re
import pymongo
import csv
from pymongo import MongoClient

def connect():
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client['Tweets']
	return client,db

def write_to_csv():
	infile = open("data.json","r")
	data = json.load(infile)
	non_eng_count = 0
	q_count = 0
	with open('data.csv', 'wb') as csvfile:
		tweet_writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		tweet_writer.writerow(['tweet_id', 'tweet_text', 'language','is_question'])
		for item in data:
			is_question = ''
			if item["language"] == "en":
				if re.search('\?',item["tweet"]):
					is_question = 'yes'
					q_count +=1 
				try:
					tweet_writer.writerow([str(item["tweet_id"]), item["tweet"].encode("utf-8"), str(item["language"]),is_question])
				except Exception, e:
					print item
					# raise e
					count+=1
			else:
				non_eng_count+=1
		print "non_eng_count:",non_eng_count
		print "q_count:",q_count
				


def write_to_db():
	client, db = connect()
	infile = open("data.json","r")
	data = json.load(infile)
	print "Got Tweets, putting in mongodb" 
	
	for item in data:
		tweets = db.tweets.insert(item)
		
	print "Done  putting in mongodb" 

if __name__ == "__main__":
	# write_to_csv()


