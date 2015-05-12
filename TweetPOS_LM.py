import csv
import CMUTweetTagger
import json
import codecs
import re
import nltk
from collections import defaultdict

class TweetPOS_LM:
    def __init__(self):
      self.trainFile = 'Train1.csv'
      self.tagFile = 'tweet_tags_15k.json'
      self.featureFile = 'postags_features_15k.json'
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
          for row in tweetreader:
              self.tweet_id.append(row[0])
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
        i = 0
        for sent in sent_tags:
            unigrams = [tag_tuple[1] for tag_tuple in sent]
            bigrams = set(nltk.bigrams(unigrams))
            trigrams = set(nltk.trigrams(unigrams))
            self.tweet_unigram[self.tweet_id[i]] = set(unigrams)
            self.tweet_bigram[self.tweet_id[i]] = bigrams
            self.tweet_trigram[self.tweet_id[i]] = trigrams

            self.tweet_feature_list.extend(unigrams)
            self.tweet_feature_list.extend(bigrams)
            self.tweet_feature_list.extend(trigrams)

            i += 1
        #json.dump(self.tweet_unigram,fil_tweet)
        self.tweet_feature_list = list(set(self.tweet_feature_list))

    def pos_tagger_writer(self):
        tweets = []
        for tw in self.tweet_original:
            try:
                tw = tw.decode('unicode_escape').encode('ascii','ignore')
            except:
                tw = re.sub(r'\\+', '', tw)
                tw = tw.decode('unicode_escape').encode('ascii','ignore')
            tweets.append(tw)

        # tweets = [tw.encode('utf8') for tw in self.tweet_original[:3]]
        tweet_tags = {}
        sent_tags = CMUTweetTagger.runtagger_parse(tweets)
        fil_tweet = open(self.tagFile,'w')
        i = 0
        for sent in sent_tags:
            is_question = 1 if self.is_question[i] == "yes" else 0
            is_anserable = 1 if self.is_answerable[i] == "yes" else 0
            pos = {"tags":sent, "is_question":is_question, "is_answerable":is_anserable}
            tweet_tags[self.tweet_id[i]] = pos
            i += 1
        json.dump(tweet_tags,fil_tweet)

    def get_features(self):
        feature_index = {}
        i = 0
        for feature in self.tweet_feature_list:
            feature_index[feature] = i
            i += 1
        i = 0
        for tweet in self.tweet_id:
            # feature_dict = {}
            features = [0,]*len(feature_index)
            for unigram in self.tweet_unigram[tweet]:
                features[feature_index[unigram]] = 1
            for bigram in self.tweet_bigram[tweet]:
                features[feature_index[bigram]] = 1
            for trigram in self.tweet_trigram[tweet]:
                features[feature_index[trigram]] = 1
            is_question = 1 if self.is_question[i] == "yes" else 0
            is_anserable = 1 if self.is_answerable[i] == "yes" else 0
            self.tweet_features[tweet] = {"features":features, "is_question":is_question, "is_answerable":is_anserable}
            i += 1
        fil_tweet = open(self.featureFile,'w')
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

    # def pos_tagger_reader(self):
    #
    #     f = open(self.tagFile,'r')
    #     tweet_tags = json.load(f)
    #     for tweet_id in in tweet_tags:
    #         sent = tweet_tags[tweet_id]["tags"]
    #         label = tweet_tags[tweet_id]["label"]
    #
    #         self.tweet_unigram[i] = set([])
    #         unigrams = [tag_tuple[1] for tag_tuple in sent]
    #         bigrams = set(nltk.bigrams(unigrams))
    #         trigrams = set(nltk.trigrams(unigrams))
    #         self.tweet_unigram[i] = set(unigrams)
    #         self.tweet_bigram[i] = bigrams
    #         self.tweet_trigram[i] = trigrams
    #
    #         self.tweet_feature_list.extend(unigrams)
    #         self.tweet_feature_list.extend(bigrams)
    #         self.tweet_feature_list.extend(trigrams)







if __name__ == "__main__":
    tp = TweetPOS_LM()
    tp.readTweets()
    #tp.pos_tagger_writer()
    tp.pos_tagger()
    tp.get_features()
