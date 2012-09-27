import probability_model
import operator
import re

# This class holds the logic for handling an incoming message
# using the probabiity table provided by the probability model

# Get the probability table
probability_table = probability_model.establish_model()

# This method takes the text of an incoming email and returns
# a boolean determining whether or not it should be filtered.
# True means the email IS spam.
def check_incoming(email_text):
	# Split the email in the same manner as in the prob model
	# and sort them by interest. Take the top 15
	tokens = re.split("[^a-zA-Z\d\$\'-]", email_text.lower())
	tokens.sort(key=define_interesting)
	tokens = tokens [-15:]

	token_probabilities = [get_probability(token) for token in tokens]
	token_pi = reduce(operator.mul,token_probabilities)
	conjugate_pi = reduce(operator.mul, [1-token_probability for token_probability in token_probabilities])
	value = token_pi/(token_pi+conjugate_pi)
	return value > 0.9


# This method is a way of getting the probability of an incident
# word and gracefully handling if it has not been seen before.
def get_probability(word):
	if word not in probability_table:
		return .4
	return probability_table[word]

# This method is a shortcut for computing the "interest" of a word
# based on its distance from 50%. 
def define_interesting(word):
	return abs(.5 - get_probability(word))