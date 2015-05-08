import csv
import CMUTweetTagger
import json
import codecs
import re
import nltk
from collections import defaultdict

class TweetPOS_LM:
    def __init__(self):
      self.trainFile = 'Train.csv'
      self.tweet_id = []
      self.tweet_original = []
      self.is_question = []
      self.is_answerable = []
      self.tweet_unigram = defaultdict(set)
      self.tweet_bigram = defaultdict(set)
      self.tweet_trigram = defaultdict(set)
      self.tweet_feature_list = []
      self.tweet_features = {}


    def readTweets(self):
      with open(self.trainFile, 'rb') as csvfile:
          tweetreader = csv.reader(csvfile, delimiter=',', quotechar='"')
          header = tweetreader.next()
          i = 1
          for row in tweetreader:
              self.tweet_id.append(i)
              i += 1
              self.tweet_original.append(row[1])
              self.is_question.append(row[2])
              self.is_answerable.append(row[3])

    def pos_tagger(self):
        tweets = []
        for tw in self.tweet_original:
            try:
                tw = tw.decode('unicode_escape').encode('ascii','ignore')
            except:
                tw = re.sub(r'\\+', '', tw)
                tw = tw.decode('unicode_escape').encode('ascii','ignore')
            tweets.append(tw)

        # tweets = [tw.encode('utf8') for tw in self.tweet_original[:3]]
        sent_tags = CMUTweetTagger.runtagger_parse(tweets)
        # fil_tweet = open('tweet_tags.json','w')
        i = 1
        for sent in sent_tags:
            self.tweet_unigram[i] = set([])
            unigrams = [tag_tuple[1] for tag_tuple in sent]
            bigrams = set(nltk.bigrams(unigrams))
            trigrams = set(nltk.trigrams(unigrams))
            self.tweet_unigram[i] = set(unigrams)
            self.tweet_bigram[i] = bigrams
            self.tweet_trigram[i] = trigrams

            self.tweet_feature_list.extend(unigrams)
            self.tweet_feature_list.extend(bigrams)
            self.tweet_feature_list.extend(trigrams)

            i += 1
        #json.dump(self.tweet_unigram,fil_tweet)
        self.tweet_feature_list = list(set(self.tweet_feature_list))


    def get_features(self):
        feature_index = {}
        i = 0
        for feature in self.tweet_feature_list:
            feature_index[feature] = i
            i += 1

        for tweet in self.tweet_id:
            # feature_dict = {}
            self.tweet_features[tweet] = [0,]*len(feature_index)
            for unigram in self.tweet_unigram[tweet]:
                self.tweet_features[tweet][feature_index[unigram]] = 1
            for bigram in self.tweet_bigram[tweet]:
                self.tweet_features[tweet][feature_index[bigram]] = 1
            for trigram in self.tweet_trigram[tweet]:
                self.tweet_features[tweet][feature_index[trigram]] = 1
        fil_tweet = open('tweet_features.json','w')
        json.dump(self.tweet_features,fil_tweet)

    def read_csv_tweets(self):
        delimiter = ';'
        i = 1
        reader = codecs.open('Train.csv', 'r', encoding='utf-8')
        for line in reader:
            print line
            row = line.split(delimiter)

            self.tweet_id.append(i)
            i += 1
            self.tweet_original.append(row[1])
            self.is_question.append(row[2])
            self.is_answerable.append(row[3])




if __name__ == "__main__":
    tp = TweetPOS_LM()
    tp.readTweets()
    tp.pos_tagger()
    tp.get_features()
