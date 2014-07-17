import sys
import json




##--------------------------------------------------------------------

def main():

	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])

	##cascading use of lists within functions

	score_dictionary = build_dic(sent_file)
	tweet_components = obtain_tweets(tweet_file)
	tweet_strings = twitter_strings(tweet_components)
	tweet_text_components = text(tweet_strings)

	scores = composite_scores(tweet_text_components,score_dictionary)
	count = 0
	for score in scores:
		print score
##--------------------------------------------------------------------






'''Function creates a of scores that reflects input list of 
	strings. '''

def composite_scores(all_tweets, word_dict):
	scores = []
	for tweet in all_tweets:
		score = tweet_score(tweet, word_dict)
		scores.append(score)
	return scores


'''Compute the score of a tweet string by comparing each word to the 
	dictionary of word scores provided. If word is not in dictionary
	(i.e. non english words) then it will receive a score of 0

	Arguments: 1) One tweet = list of words [].
			   2) Word dictionary'''

def tweet_score(my_tweet, word_dict):
	score = 0
	for word in my_tweet:
		if word in word_dict:
			value = word_dict[word]
		else: 
			value = 0
		score+=value
	return score

'''Function used to build a dictionary of word: score values'''
def build_dic(fp):
	## Build a dictionary from 'AFFINN-111.txt'
	scores = {}
	for line in fp:
		pair = line.split("\t") #tab delimited file
		word = pair[0]
		my_int = int(pair[1])
		scores[word] = my_int
	return scores

'''Nearly identical to above function, but returns a list of strings'''
def twitter_strings(twitter_list):
	tweets = []
	for tweet in twitter_list:
		tweet_text = tweet["text"]
		tweets.append(tweet_text)
	return tweets


'''Create a list of twitter text elements from each twitter dictionary
	this list will actually be a list of lists because we will parse the 
	twitter strings by word'''
def text(twitter_strings):
	tweets = []
	for string in twitter_strings:
		text_words = string.split(" ")
		tweets.append(text_words)
	return tweets



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



if __name__ == '__main__':
    main()
