from nltk.corpus import wordnet as wn
# import nltk
import re, json

'''
-	Extract words from a tweet
-	Run a synonym generator and extract synonym words
-	Run hypernym generation and exract words
-	write to the csv
'''

twitter_parser_to_wordnet_map = {
	u'N':wn.NOUN,
	u'^':wn.NOUN,
	u'A':wn.ADJ,
	u'V':wn.VERB,
	u'L':wn.VERB
}

def get_final_pos_words(pos_words):
	'''
	-	for each pos_tuple
		-	Remove noun type (return [])
		-	replace # and 's with ''
	- return final words
	'''

	final_pos_words = []
	for pos_tuple in pos_words:
		if pos_tuple[1] == u'N' or pos_tuple[1] == u'@' or pos_tuple[1] == u'U' or pos_tuple[1] == u'E' or pos_tuple[1] == u'^':
			continue
		temp_word = re.sub('s?|#','',pos_tuple[0])
		final_pos_words.append([temp_word,pos_tuple[1]])
	# print len(final_pos_words)
	return final_pos_words

def get_wordnet_features(word, pos_tag):
	# print 'Processing:',word
	try:
		word_synsets = wn.synsets(word, twitter_parser_to_wordnet_map[pos_tag])
	except Exception, e:
		word_synsets = wn.synsets(word)
	
	synonyms = []
	hypernyms = []
	hypernym_synset = []
	for w_s in word_synsets:
		synonyms.append(str(w_s._name))
		hypernym_synset.extend(w_s.hypernyms())
	for h_s in hypernym_synset:
		hypernyms.append(str(h_s._name))
	# print '\tSynonyms',synonyms
	# print '\tHypernym',hypernyms
	return synonyms, hypernyms

def get_all_pos_words(tagged_tweets):
	'''
		-	Get all the pos tags and find uniq set
		-	run wordnet syn and hyp and print to file
	'''
	pos_words = []
	for tweet_id in tagged_tweets:
		pos_words.extend(tagged_tweets[tweet_id][u'tags'])
	# print 'POS words:',len(pos_words)
	return pos_words

def get_global_wordnet_tags(tagged_tweets):
	'''
		-	Get all pos Words
		-	For each word find synonyms and hypernyms and form a list of it all.
	'''

	pos_words = get_all_pos_words(tagged_tweets)
	final_pos_words = get_final_pos_words(pos_words)
	print 'Extacting ALL pos words:',len(pos_words)
	print 'Extacting FILTERED pos words:',len(final_pos_words)
	synonyms = []
	hypernyms = []
	print 'Getting synonyms and hypernyms...'
	for index,word_tuple in enumerate(final_pos_words):
		if index%10000 == 0:
			print '\tprocessing',index
		temp_syn, temp_hyp = get_wordnet_features(word_tuple[0],word_tuple[1])
		synonyms.extend(temp_syn)
		hypernyms.extend(temp_hyp)
	# print 'synonyms len:',len(synonyms),'hypernyms len:',len(hypernyms)
	syn_set = set(synonyms)
	hyp_set = set(hypernyms)
	print 'syn_set len:',len(syn_set),'hyp_set len:',len(hyp_set)
	return list(syn_set), list(hyp_set)

def get_wordnet_tagged_tweets(tagged_tweets):
	print 'Processing tweets:'
	# print tagged_tweets
	wordnet_tagged_tweets = {}
	count = 0
	for index, pos_dict in tagged_tweets.iteritems():
		count+=1
		if count%1000 == 0:
			print '\ttweet count:',count
		tweet_syn = []
		tweet_hyp = []
		filtered_pos_list = get_final_pos_words(pos_dict[u'tags'])
		# print 'filtered_pos_list',len(filtered_pos_list)
		for pos_tuple in filtered_pos_list:
			# print pos_tuple
			temp_syn, temp_hyp = get_wordnet_features(pos_tuple[0],pos_tuple[1])
			tweet_syn.extend(temp_syn)
			tweet_hyp.extend(tweet_hyp)
		temp_features = list(set(temp_syn+temp_hyp))
		wordnet_tagged_tweets[index] = {'features':temp_features,'is_question':pos_dict[u'is_question'], 'is_answerable':pos_dict[u'is_answerable']}
		# print wordnet_tagged_tweets
		# break
	# print 'len:',len(wordnet_tagged_tweets.keys())
	return wordnet_tagged_tweets

def get_final_tweet_feature_vector(wordnet_tagged_tweets, wordnet_features):
	'''
		-	create a defalut vector with 0's
		-	check of the feature is present in the word feature
		-	tag turn it on, else off
	'''
	print 'Generating final features...'
	final_tweet_vector = {}
	wordnet_feature_dict = {}
	count = 0

	for index,w_feature in enumerate(wordnet_features):
		wordnet_feature_dict[w_feature] = index

	for index, wordnet_dict in wordnet_tagged_tweets.iteritems():
		# print wordnet_dict
		count+=1
		# print wordnet_values
		if count%1000 == 0:
			print '\ttweet:',count
		tweet_features = [0]*len(wordnet_features)
		# print tweet_features
		wordnet_values = wordnet_dict['features']
		for w_val in wordnet_values:
			tweet_features[wordnet_feature_dict[w_val]] = 1
		# print 'sum:',sum(tweet_features)
		final_tweet_vector[index] = {'features':tweet_features,'is_question':wordnet_dict[u'is_question'],'is_answerable':wordnet_dict[u'is_answerable']}
	# print final_tweet_vector
	return final_tweet_vector


def process_tweets():
	'''
		-	Generate global list of synonyms and hypernyms
		- 	For each tweet get wordnet features
		-	Check agains global wordnet features and mark as 1 if present
	'''

	tagged_file = open("tweet_tags_15k.json","r")
	tagged_tweets = json.load(tagged_file)
	tagged_file.close()
	# print tagged_tweets
	synonyms, hypernyms = get_global_wordnet_tags(tagged_tweets)
	wordnet_features = list(set(synonyms+hypernyms))
	# print 'wordnet_feature',wordnet_features
	wordnet_tagged_tweets = get_wordnet_tagged_tweets(tagged_tweets)
	final_tweet_vector = get_final_tweet_feature_vector(wordnet_tagged_tweets, wordnet_features)

	print "Writing into file..."
	wordnet_output = open('wordnet_tags_15k.json','w')
	json.dump(final_tweet_vector,wordnet_output)
	wordnet_output.close()

if __name__ == '__main__':
	process_tweets()