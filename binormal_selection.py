import numpy as np
import json
import csv
import sys
from collections import Counter, defaultdict
from scipy.stats import norm
from operator import itemgetter


def load_features_and_labels(filename):
    print "\nStage: Load Features"
    #Feature1
    infile1 = open(filename,"r")
    feature1 = json.load(infile1)
    infile1.close()
    return feature1




##### Input feature_dict is a dictionary where the keys are tweet IDs and the value is a tuple/list of feature vector, label
##### Output is bns_features which is a dictionary of feature id (just an index number) and the BNS value.
def count_metrics(feature_dict, label_type, bns_filename):
    vals = feature_dict.values()
    tweet_features = [f_tuple["features"] for f_tuple in vals]
    tweet_labels = [f_tuple[label_type] for f_tuple in vals]
    num_features = len(tweet_features[0])
    label_counts = Counter(tweet_labels)
    pos = label_counts[1]
    neg = label_counts[0]
    print 'num_features',num_features
    print 'pos',pos
    print 'neg',neg

    true_pos = defaultdict(int)
    true_neg = defaultdict(int)
    false_pos = defaultdict(int)
    false_neg = defaultdict(int)

    true_pos_rate = {}
    false_pos_rate = {}

    np_labels = np.array(tweet_labels)
    for i in xrange(num_features):
        if i%1000 == 0:
            print 'Calculating',i,'of',num_features,'...'
        vals = [features[i] for features in tweet_features]
        # print vals
        np_vals = np.array(vals)
        true_pos[i] = np.sum(np.logical_and(np_vals, np_labels))
        false_pos[i] = np.sum(np.logical_and(np_vals, np.logical_not(np_labels)))
        true_pos_rate[i] = float(true_pos[i])/pos
        false_pos_rate[i] = float(false_pos[i])/neg

    bns_features = {}
    for i in xrange(num_features):
        if i%1000 == 0:
            print 'Calculating',i,'of',num_features,'...'
        print 'generating bns_features',i,'of',num_features,'...'
        if true_pos_rate[i] != 0 and false_pos_rate[i] != 0 and true_pos_rate[i] != 1 and false_pos_rate[i] != 1:
            bns_features[i] = abs(norm.ppf(true_pos_rate[i]) - norm.ppf(false_pos_rate[i]))

    top_features = sorted(bns_features, key=bns_features.get, reverse=True)
    f = open(bns_filename, "w")
    json.dump(top_features, f)

if __name__ == "__main__":
    features = load_features_and_labels("lexical_tags_15k.json")
    print 'getting bns scores for is_question...'
    label_type = "is_question" 
    bns_filename = "lexical_bns_scores_"+label_type+".json"
    count_metrics(features, label_type, bns_filename)
    print 'getting bns scores for is_answerable...'
    label_type = "is_answerable" 
    bns_filename = "lexical_bns_scores_"+label_type+".json"
    count_metrics(features, label_type, bns_filename)

