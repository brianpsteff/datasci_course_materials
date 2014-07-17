
'''Execution: python happiest_state.py AFINN-111.txt output.txt states.json
'''



import sys
import json
import codecs



def main():

	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	word_scores = build_dic(sent_file)

	tweets_to_evaluate = filter_tweets(tweet_file)

	

	separated_tweets = categorize_tweets(tweets_to_evaluate)


	states_and_scores = state_scores(separated_tweets, states, word_scores)

	'''Now to determine the state with the highest composite 
	twitter sentiment score!!!!'''

	highest_score = 0
	winning_state = ''

	for state in states_and_scores:
		score = list_sum(states_and_scores[state])
		if score > highest_score:
			highest_score = score
			winning_state = state

	


	winning_state.strip()
	my_state = winning_state.encode('utf-8')
	new_state = my_state[1:]
	print new_state
	



def list_sum(my_list):
	my_sum = 0
	for integer in my_list:
		my_sum += integer
	return my_sum

'''This will compress the separated tweets into a dictionary of 
of state keys and a value list of integer text scores'''
def state_scores(tweets_by_state, list_of_states, word_scores):
	states_scores = {}
	for state in tweets_by_state:
		list_scores = tweet_to_score(tweets_by_state[state], word_scores)
		states_scores[state] = list_scores
	return states_scores



'''Takes a list of tweet data structures as a argument and returns a list
	of scores for each tweet'''
def tweet_to_score(tweet_list, word_scores):
	text_scores = []
	for tweet in tweet_list:
		string = tweet["text"]
		word_list = string.split(' ')
		score = tweet_score(word_list, word_scores)
		text_scores.append(score)

	return text_scores



'''Key field is the state and value field is a list of twitter data structures
	'''
def categorize_tweets(my_tweets):
	separated_tweets = {}
	for tweet in my_tweets:
		location = tweet["place"]["full_name"]
		city_state = location.split(",")
		state = city_state[1]
		if state in separated_tweets:
			separated_tweets[state].append(tweet)
		else:
			separated_tweets[state] = [tweet]
	return separated_tweets
				
				
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


'''This funtion is used to only allow the loading of tweets that:
	- contain text and place values
	- are in english
	- are within the United States
'''
def filter_tweets(file):
	to_evaluate = []
	for line in file:
		current_tweet = json.loads(line)
		if "text" and "place" and "lang" in current_tweet:
			if current_tweet["lang"]=="en" and current_tweet["place"] != None:			
				country = current_tweet["place"]["country"]
				if country == 'United States' :
					to_evaluate.append(current_tweet)
	return to_evaluate

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


'''Coursera provided state dictionary'''

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}



if __name__ == '__main__':
	main()





