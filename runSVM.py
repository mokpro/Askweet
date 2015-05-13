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
    accuracy = clf.score(X_test, y_test)
    # print 'clf.score:',accuracys
    #classifier = svm.SVR(kernel='linear')
    #classifier.fit(X[:1000], Y[:1000])
    # print " the predictions"
    
    return accuracy

def load_json(filename):
    print "\nStage: Load Features"
    #Feature1
    json_file = open(filename,"r")
    new_json = json.load(json_file)
    json_file.close()

    return new_json

def select_top_k_features(feature_dict, k, label_type,bns_scores):
    top_features = bns_scores[:k]
    tweet_features = []
    tweet_labels = []
    for tweet_id,features in feature_dict.iteritems():
        feature_list_n = numpy.array(features["features"])
        feature_list_k = feature_list_n[top_features]
        tweet_features.append(feature_list_k)
        tweet_labels.append(features[label_type])

    return (tweet_features, tweet_labels)

def run_svm_for_bns_features(feature_type):
    '''
    Run svm for k values 0 to 4000 with interval 
    Return 
    result = {
        "postags":{
            "is_question":{
                500:087,
                1000:0,84,
                .
                .
                .

            }
        }
    }
    '''
    feature_dict = load_json(feature_type+"_features_15k.json")
    label_type_list = ["is_question","is_answerable"]
    result = {}

    print "Running for feature type",feature_type

    for label_type in label_type_list:
        print "Running svm for label:",label_type,"\n\n"
        bns_scores = load_json(feature_type+"_bns_scores_"+label_type+".json")
        result[label_type] = {}

        k =len(bns_scores)
        # print bns_scores
        print 'k:'+str(k)
        (features_k, labels_k) = select_top_k_features(feature_dict, k, label_type, bns_scores)
        accuracy = run_svm(features_k, labels_k)
        print 'accuracy:'+str(accuracy)
        result[label_type][k] = accuracy

        for k in xrange(200,len(bns_scores),200):
            print 'k:'+str(k)
            (features_k, labels_k) = select_top_k_features(feature_dict, k, label_type, bns_scores)
            accuracy = run_svm(features_k, labels_k)
            print 'accuracy:'+str(accuracy)
            result[label_type][k] = accuracy

    return result

def run_svm_for_all_features(feature_type):

    feature_dict = load_json(feature_type+"_features_15k.json")
    label_type_list = ["is_question","is_answerable"]
    result = {}

    for label_type in label_type_list:
        tweet_features = []
        tweet_labels = []
        for tweet_id,features in feature_dict.iteritems():
            feature_list_n = numpy.array(features["features"])
            tweet_features.append(feature_list_n)
            tweet_labels.append(features[label_type])

        print "Running svm for label:",label_type,"\n\n"
        result[label_type] = {}
        accuracy = run_svm(tweet_features, tweet_labels)
        result[label_type] = accuracy
    return result

if __name__ == "__main__":
    print "\nStage: Init Program"
    # all the differnt types of X's for the SVM
    #feature1, feature2, feature3, allFeatures = load_features()
    feature_type_list = ["postags","wordnet","lexical"]
    result = {}

    # for feature_type in feature_type_list:
    #     result[feature_type]['bns_features'] = run_svm_for_bns_features(feature_type)
    # print result
    
    for feature_type in feature_type_list:
        result[feature_type] = {}
        result[feature_type]['all_features'] = run_svm_for_all_features(feature_type)
    print result


