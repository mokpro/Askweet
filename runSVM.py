import json
from collections import defaultdict
from sklearn import svm
from sklearn import cross_validation
import csv
import numpy

def run_svm(feature, labels):
    '''Fitting a classifier using SVM Regression and predicting the values
            using linear kernel and perform five fold cross validation
    '''
    print "\nStage: SVM"

    X = feature
    Y = labels
    X_train, X_test, y_train, y_test = cross_validation.train_test_split( X, Y, test_size=0.3, random_state=0)

    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    print clf.score(X_test, y_test)
    #classifier = svm.SVR(kernel='linear')
    #classifier.fit(X[:1000], Y[:1000])
    print " the predictions"

def load_features(filename):
    print "\nStage: Load Features"
    #Feature1
    infile1 = open(filename,"r")
    feature_dict = json.load(infile1)
    infile1.close()


    return feature_dict


def select_top_k_features(feature_dict, k, label_type, bns_filename):
    infile1 = open(bns_filename,"r")
    bns_scores = json.load(infile1)
    top_features = bns_scores[:k]

    tweet_features = []
    tweet_labels = []
    for tweet_id,features in feature_dict.iteritems():
        feature_list_n = numpy.array(features["features"])
        feature_list_k = feature_list_n[top_features]
        tweet_features.append(feature_list_k)
        tweet_labels.append(features[label_type])

    return (tweet_features, tweet_labels)


if __name__ == "__main__":
    print "\nStage: Init Program"
    # all the differnt types of X's for the SVM
    #feature1, feature2, feature3, allFeatures = load_features()
    feature_dict = load_features("postags_features_15k.json")
    k = 500
    label_type = "is_question"
    bns_filename = "feature_bns_scores_"+label_type+".json"
    (features_k, labels_k) = select_top_k_features(feature_dict, k, label_type, bns_filename)
    run_svm(features_k, labels_k)
