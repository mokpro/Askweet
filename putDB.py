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
	count = 0
	non_eng_count = 0
	q_count = 0
	with open('data.csv', 'wb') as csvfile:
		tweet_writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		tweet_writer.writerow(['tweet_id', 'tweet_original','tweet_clean','language','has_question_word','question_word'])
		for item in data:
			tweet_clean = clean_the_tweet_text(item["tweet"])
			has_question_word = ''
			question_word = ''
			question_words = ['?', 'when', 'why', 'where', 'which', 'how', 'what', 'who']

			if item["language"] == "en":
				for q_word in question_words:
					if  q_word in item["tweet"].lower().split(' '):
						has_question_word = 'yes'
						question_word = q_word
						q_count+=1
				try:
					tweet_writer.writerow([str(item["tweet_id"]), item["tweet"].encode("utf-8"),tweet_clean, str(item["language"]),has_question_word, question_word])
				except Exception, e:
					print item
					# raise e
					count+=1
			else:
				non_eng_count+=1
		print "count:",count
		print "q_count:",q_count
				
def clean_the_tweet_text(raw_tweet):
	clean_tweet = raw_tweet.lower().encode("utf-8")
	regex_form = '^rt\s+|@\w+:*|https?://[\w\.\/]*'
	clean_tweet = re.sub(regex_form, '', clean_tweet)
	return clean_tweet

def write_to_db():
	client, db = connect()
	infile = open("data.json","r")
	data = json.load(infile)
	print "Got Tweets, putting in mongodb" 
	
	for item in data:
		tweets = db.tweets.insert(item)
		
	print "Done  putting in mongodb" 

if __name__ == "__main__":
	write_to_csv()