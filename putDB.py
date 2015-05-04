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

def read_tweets_file(filename):
	# Read the tweets file and generate a list of dictionaries with keys as follows
	# dictionary keys ---> 'tweet_id', 'tweet', 'language'

	print "Reading tweets file"
	infile = open(filename,"r")
	data = infile.read().split('\n')[:-1]
	tweets = []

	for temp in data:
		try:
			item = json.loads(temp)
			#print item
			tweet = item["text"]
			ids = item["id"]
			lang = item["lang"]
			tweets.append({'tweet_id':ids,'tweet':tweet,'language':lang})
		except:
			continue

	print len(tweets), "Extracted"
	return tweets

def write_to_csv(data):
	#infile = open("data-bala.json","r")
	#data = json.load(infile)
	count = 0
	non_eng_count = 0
	q_count = 0
	with open('data-bala.csv', 'wb') as csvfile:
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

def tweet_analyzer(tweets):
    qwords = set(['who', 'what', 'when', 'where', 'why', 'how', 'do', 'is', 'could', 'can', "can't", 'cant', 'would', "wouldn't", "wouldnt", 'should', "shouldn't", "shouldnt", 'did', 'will', 'has', 'have', "won't", 'does', 'wont', 'doesnt', "doesn\'t", 'had', 'are'])
    data = []
    count = 0
    for item in tweets:
        if '?' in item['tweet']:
            data.append(item['tweet'])
            continue
        temp = item['tweet'].lower().split()
        while(temp[0][0] == '@' or temp[0] == 'rt' or temp[0][0] == '#' ):
            temp = temp[1:]
        for word in qwords:
            if word in temp[0]:
                data.append(temp)
                break
    print len(data)

if __name__ == "__main__":
	data = read_tweets_file("tweets_file_apr27.txt")
	write_to_csv(data)
