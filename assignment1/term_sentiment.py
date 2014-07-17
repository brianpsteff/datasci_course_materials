import sys
import json

##--------------------------------------------------------------------

def main():

	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	'''cascading use of lists within functions, set the stage for 
	further textual analysis'''
	word_sent_dic = build_dic(sent_file)	#Dictionary
	tweets = obtain_tweets(tweet_file) #List
	tweet_string = tweets_string(tweets)  #List
	tweet_words = tweets_words(tweet_string)	#List
	scores = tweet_scores(tweet_words,word_sent_dic) #List
	
	new_words = {}

	for i in range(0, len(tweets)):
		find_words(tweet_words[i], word_sent_dic, new_words, scores[i])

	newWord_sent_dic = dictionary_consolidation(new_words)
	print_dict(newWord_sent_dic)

##--------------------------------------------------------------------

'''Function that returns a list of tweet dictionaries by using
	json.loads'''
def obtain_tweets(fp):
	json_tweets = []
	for line in fp:
		tweet_data = json.loads(line)
		my_key = "text"
		#We only want to append twitter dictionaries that contain a 'text field'
		if my_key in tweet_data:
			json_tweets.append(tweet_data)

	return json_tweets

##FUCTIONS ASSOCIATED WITH COMPUTING NEW SCORES############################

'''Function that takes list of words that are part of a tweet string
	Check each word to see if it is in dictionary of already ranked words
	if not:
		if in unranked words:
			add the composite tweet score to key value list
		else:
			create new key with exactly one score in value list

	Arguments: (1) tweet_word_list = A single tweet text split into a list of words
			   (2) ranked_dictionary = dic built from AFFINN-111
			   (3) unranked_dictionary = bin to store new words
			   (4) score = score of current tweet

	'''
def find_words(tweet_word_list, ranked_dictionary, unranked_dictionary, tweet_score):
	for word in tweet_word_list:
		if word not in ranked_dictionary:
			if word in unranked_dictionary:
				unranked_dictionary[word].append(tweet_score)
			else:
				unranked_dictionary[word] = [tweet_score]


'''Function that sums each value in a list'''
def list_sum(my_list):
	my_sum = 0
	for value in my_list:
		my_sum += value
	return my_sum


'''Function that takes dictionary of string keys and integerlist values
	and returns a dictionary of string keys and integer values that are equal
	to the summation of the integers in list.'''

def dictionary_consolidation(my_dictionary):
	word_value = {}
	for key in my_dictionary:
		value = list_sum(my_dictionary[key])
		word_value[key] = value
	return word_value


'''Function used to print all the new words with their respective
	sentiment scores'''
def print_dict(my_dict):
	for key in my_dict:
		if my_dict[key] != 0:
			print '%s %d'%(key, my_dict[key])



#######################################################################



##FUNCTIONS TO PERFORM BASIC TEXTUAL EVALUATION#######################

'''Function creates a list of scores that reflects input list of 
	strings. '''

def tweet_scores(tweets, score_dict):
	scores = []
	for tweet in tweets:
		score = tweet_score(tweet, score_dict)
		scores.append(score)
	return scores



'''Compute the score of a tweet string by comparing each word to the 
	dictionary of word scores provided. If word is not in dictionary
	(i.e. non english words) then it will receive a score of 0

	Arguments: 1) One tweet = list of words [].
			   2) Word dictionary'''
def tweet_score(tweet_words, score_dict):
	score = 0
	for word in tweet_words:
		if word in score_dict:
			value = score_dict[word]
		else: 
			value = 0
		score+=value
	
	return score


'''Function used to build a dictionary of word: score values'''
def build_dic(in_file):
	## Build a dictionary from 'AFFINN-111.txt'
	scores = {}
	for line in in_file:
		pair = line.split("\t") #tab delimited file
		word = pair[0]
		my_int = int(pair[1])
		scores[word] = my_int
	return scores

'''Returns a tweet in string format'''
def tweets_string(tweets_list):
	tweets = []
	for tweet in tweets_list:
		string = tweet["text"]
		tweets.append(string)
	return tweets


'''Create a list of twitter text elements from each twitter dictionary
	this list will actually be a list of lists because we will parse the 
	twitter strings by word'''
def tweets_words(twitter_strings):
	tweets = []
	for string in twitter_strings:
		words = string.split(" ")
		tweets.append(words)
	return tweets

######################################################################





if __name__ == '__main__':
    main()
