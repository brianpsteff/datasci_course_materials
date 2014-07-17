import sys
import json


def main():

	tweet_file = open(sys.argv[1])
	tweet_objects = obtain_tweets(tweet_file)
	#filtered_tweets = filter_tweets(tweet_objects)
	deconstructed_tweets = deconstruct_tweet(tweet_objects)

	word_dictionary = build_dictionary(deconstructed_tweets)

	#Calculate total number of words
	word_total = 0
	for word in word_dictionary:
		local_frequency = word_dictionary[word]
		word_total += local_frequency

	#Create a list of tupels
	word_list = word_dictionary.items()
	
	for i in range(0, len(word_list)):
		word = word_list[i][0]
		word2 = word.encode('utf-8')
		occurrence = word_list[i][1]/(float(word_total))
		print '%s %f'%(word2,occurrence)
		

'''Takes a list of words that compose ONE tweet and updates count of existing
		words or adds new words to the dictionary'''
def update_dictionary(tweet_decomposition, word_dictionary):
	for word in tweet_decomposition:
		if word in word_dictionary:
			word_dictionary[word] += 1
		else:
			word_dictionary[word] = 1


'''Takes the list of deconstructed tweets as an argument and builds the 
		appropriat word frequency dictionary'''
def build_dictionary(my_tweets):
	word_dictionary = {}
	for tweet in my_tweets:
		update_dictionary(tweet, word_dictionary)
	return word_dictionary


'''List of tweets separated into their respective lists of words 
		separated by white space'''
def deconstruct_tweet(my_tweets):
	word_list = []
	for tweet in my_tweets:
		each_word = tweet["text"].split() # Could be improved by using RegExpression
		word_list.append(each_word)
	return word_list

'''Only take english tweets into consideration
def filter_tweets(my_tweets):
	exacutables = []
	for tweet in my_tweets:
		if tweet["lang"] == "en":
			exacutables.append(tweet)
	return exacutables'''

'''Function that returns a list of tweet dictionaries by using
	json.loads'''
def obtain_tweets(my_file):
	json_tweets = []
	for line in my_file:
		tweet_data = json.loads(line)
		if "text" and "lang" in tweet_data:
			json_tweets.append(tweet_data)
	return json_tweets


if __name__ == '__main__':
	main()