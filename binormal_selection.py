import numpy as np
from collections import Counter, defaultdict
from scipy.stats import norm


##### Input feature_dict is a dictionary where the keys are tweet IDs and the value is a tuple/list of feature vector, label
##### Output is bns_features which is a dictionary of feature id (just an index number) and the BNS value.
def count_metrics(feature_dict):
    vals = feature_dict.values()
    tweet_features = [f_tuple[0] for f_tuple in vals]
    tweet_labels = [f_tuple[1] for f_tuple in vals]
    num_features = len(tweet_features[0])
    label_counts = Counter(tweet_labels)
    pos = label_counts[1]
    neg = label_counts[0]

    true_pos = defaultdict(int)
    true_neg = defaultdict(int)
    false_pos = defaultdict(int)
    false_neg = defaultdict(int)

    true_pos_rate = {}
    false_pos_rate = {}

    np_labels = np.array(tweet_labels)

    for i in xrange(num_features):
        vals = [features[i] for features in tweet_features]
        np_vals = np.array(vals)
        true_pos[i] = sum(np.logical_and(np_vals, np_labels))
        false_pos[i] = sum(np.logical_and(np_vals, np.logical_not(np_labels)))
        true_pos_rate[i] = true_pos[i]/pos
        false_pos_rate[i] = false_pos_rate[i]/neg

    # feature_index = {}
    # i = 0
    # for feature in tweet_feature_list:
    #     feature_index[feature] = i
    #     i += 1
    #
    # for tweet_id, tweet_features in tweet_features.iteritems():
    #     label  = tweet_labels[tweet_id]
    #     for feature in tweet_feature_list:
    #         if tweet_features[feature_index[feature]] == 1:
    #             if label == 'yes':
    #                 true_pos[feature] += 1
    #             else:
    #                 false_pos[feature] += 1
    #
    # for feature in tweet_feature_list:
    #     true_neg[feature] = neg - false_pos[feature]
    #     false_neg[feature] = pos - true_pos[feature]
    #     true_pos_rate[feature] = true_pos[feature]/pos
    #     false_pos_rate[feature] = false_pos_rate[feature]/neg

    bns_features = [abs(norm.ppf(true_pos_rate[i]) - norm.ppf(false_pos_rate[i])) for i in xrange(num_features)]
