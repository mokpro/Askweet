import csv
import re
import json
import nltk
import Stemmer
from collections import defaultdict

template_dict = lambda length, number, has_url, has_mention, coverage :{'length':length, 'number_of_words':number, 'has_url':has_url, 'has_mention':has_mention, 'coverage':coverage}

def dump_to_json(output_data):
    lexical_output = open('lexical_tags.json','w')
    json.dump(output_data,lexical_output)
    lexical_output.close()

class FeatureVectors:
    def __init__(self):
        self.featureVectors = defaultdict()

    def compute_features(self, trainData):
        stemmer = Stemmer.Stemmer('english')
        for ids in trainData.data:
            features = [0]*len(trainData.features)
            # meta features
            length, number, has_url, has_mention, coverage = (0,)*5

            #get the tweet
            tweet = trainData.data[ids]

            #get the tags
            temp = set([x[2] for x in tweet])
            #check for url and mentions
            if 'U' in temp:
                has_url = 1
            if '@' in temp:
                has_mention = 1

            #compute len of tweet and number of words
            length = sum([len(word[0]) for word in tweet])
            number = len(tweet)

            #process tweet for coverage and other Lexical features
            tweet_text = [ words[0] for words in tweet ]
            clean_tweet = ' '.join(tweet_text)
            regex_form = '^rt\s+|@\w+:*|https?://[\w\.\/]*'
            clean_tweet = re.sub(regex_form, '', clean_tweet)
            clean_tweet = [stemmer.stemWord(x) for x in clean_tweet.split()]

            #compute coverage
            coverage = len(set(clean_tweet)) / len(trainData.unigram_vocab)

            #compute lexical features
            for item in clean_tweet:
                if item in set(trainData.unigram_vocab):
                    features[trainData.featureIndex[item]] = 1

            for item in list(nltk.bigrams(clean_tweet)):
                if item in set(trainData.bigram_vocab):
                    features[trainData.featureIndex[item]] = 1

            for item in list(nltk.trigrams(clean_tweet)):
                if item in set(trainData.trigram_vocab):
                    features[trainData.featureIndex[item]] = 1

            #append the lexical and meta features
            self.featureVectors[ids] = features + [length, number, has_url, has_mention, coverage]

        print "Finished creating the Lexical and Meta Feature Vectors"

class LexicalFeatures:
    def __init__(self, filename):
        self.filename = filename
        self.featureIndex = defaultdict(int)
        self.features = []
        self.unigram_vocab = defaultdict(int)
        self.bigram_vocab  = defaultdict(int)
        self.trigram_vocab = defaultdict(int)
        self.data = {}
        self.get_data_from_file()
        self.log()

    def get_data_from_file(self):
        stemmer = Stemmer.Stemmer('english')
        infile = open(self.filename,"r")
        self.data = json.load(infile)

        for ids in self.data:
            tweet = self.data[ids]
            tweet_text = [ words[0] for words in tweet ]
            clean_tweet = ' '.join(tweet_text)
            regex_form = '^rt\s+|@\w+:*|https?://[\w\.\/]*'
            clean_tweet = re.sub(regex_form, '', clean_tweet)
            clean_tweet = [stemmer.stemWord(x) for x in clean_tweet.split()]

            for item in clean_tweet:
                self.unigram_vocab[item] += 1

            for item in list(nltk.bigrams(clean_tweet)):
                self.bigram_vocab[item] += 1

            for item in list(nltk.trigrams(clean_tweet)):
                self.trigram_vocab[item] += 1

        temp = [ k for k,v in self.unigram_vocab.iteritems() if v >= 5 ]
        self.unigram_vocab = temp

        temp = [ k for k,v in self.bigram_vocab.iteritems() if v >= 5 ]
        self.bigram_vocab = temp

        temp = [ k for k,v in self.trigram_vocab.iteritems() if v >= 3 ]
        self.trigram_vocab = temp

        self.features = self.unigram_vocab + self.bigram_vocab + self.trigram_vocab

        for index, item in enumerate(self.features):
            self.featureIndex[item] = index

        print "Finished composing the Lexical Features"


    def log(self):
        print "\nUnigram Features is %s" % (len(self.unigram_vocab))
        print "\nBigram Features is %s" % (len(self.bigram_vocab))
        print "\nTrigram Features is %s" % (len(self.trigram_vocab))
        print "\nTotal Lexical Features is %s" % (len(self.features))

if __name__ == "__main__":
    #inputFile = "Train.csv"
    inputFile = "tweet_tags.json"
    trainData = LexicalFeatures(inputFile)
    #exit()
    trainFeatureVectors = FeatureVectors()
    #trainLF.get_data_from_file()
    trainFeatureVectors.compute_features(trainData)

    dump_to_json(trainFeatureVectors.featureVectors)
