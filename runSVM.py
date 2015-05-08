import csv
import json
from collections import defaultdict
from sklearn import svm
from sklearn import cross_validation

def run_svm(feature, labels):
    '''Fitting a classifier using SVM Regression and predicting the values
            using linear kernel and perform five fold cross validation
    '''
    print "\nStage: SVM"

    X = feature.values()
    Y = labels
    X_train, X_test, y_train, y_test = cross_validation.train_test_split( X[:5000], Y[:5000], test_size=0.3, random_state=0)

    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    print clf.score(X_test, y_test)
    #classifier = svm.SVR(kernel='linear')
    #classifier.fit(X[:1000], Y[:1000])
    print " the predictions"
    """
    #predict for the test data
    for distance in test_data:
        test_data[distance] = classifier.predict([distance])

    #Dump the values
    print "\nDumping the training and test data"
    dump_csv(train_data, "Train.csv")
    dump_csv(test_data, "Test.csv")
    """
    #scores = cross_validation.cross_val_score(classifier, X, Y, cv=5)

    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

def load_features():
    print "\nStage: Load Features"
    #Feature1
    infile1 = open("lexical_tags.json","r")
    feature1 = json.load(infile1)
    infile1.close()

    #Feature4 - Combining all features
    """ #was getting killed
    #Feature2
    infile2 = open("wordnet_tags.json","r")
    feature2 = json.load(infile2)
    infile2.close()
    #Feature3
    infile3 = open("postags.json","r")
    feature3 = json.load(infile3)
    infile3.close()

    allFeatures = feature1
    for item in feature2:
        allFeatures[item].extend(feature2[item])

    for item in feature3:
        allFeatures[item].extend(feature3[item])
    """
    return feature1#, feature2, feature3, allFeatures

def load_temp_labels():
    print "\nStage: Load temp Labels"
    label = defaultdict()
    csvfile = open("Train.csv","r")
    tweetreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = tweetreader.next()
    i = 1
    for row in tweetreader:
        if row[2] == "yes":
            label[i] = 1
        else:
            label[i] = 0
        i += 1
    return label

def match_and_load_labels(feature, temp):
    print "\nStage: Match and Load Labels"
    Z = []

    for item in feature:
        Z.append(temp[int(item)])

    return Z

if __name__ == "__main__":
    print "\nStage: Init Program"
    # all the differnt types of X's for the SVM
    #feature1, feature2, feature3, allFeatures = load_features()
    feature1 = load_features()
    # Y - the labels for the SVM
    temp_labels = load_temp_labels()
    Y = match_and_load_labels(feature1, temp_labels)

    run_svm(feature1, Y)
