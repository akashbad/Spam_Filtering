import os
import re
import operator

probability_table = {}

# Internal functions, used to build dictionaries of spam data
def build_frequency_dictionary(path):
	file_paths = [path + file_name for file_name in os.listdir(path)]
	words = []
	for current_path in file_paths:
		file = open(current_path, "r")
		text = file.read()
		x = re.split("[^a-zA-Z\d\$\'-]", text.lower())
		words.extend(x)
		file.close()
	words = filter(lambda a: a != '' and not a.isdigit(),words)
	frequency_dictionary = {}
	for word in words:
		try:
			frequency_dictionary[word] += 1
		except:
			frequency_dictionary[word] = 1
	return frequency_dictionary

def merge_frequency_dictionaries(target_dictionary, other_dictionary):
	for word in other_dictionary.keys():
		if target_dictionary.has_key(word):
			target_dictionary[word] += other_dictionary[word]
		else:
			target_dictionary[word] = other_dictionary[word]

def create_probability_table(spam, ham, spam_file_num, ham_file_num):
	all_words = list(set(spam.keys()).union(set(ham.keys())))
	probabilities = {}
	for word in all_words:
		# Get the number of occurences for each word
		if word in ham:
			good_word_occurences = ham[word]
		else:
			good_word_occurences = 0
		if word in spam:
			bad_word_occurences = spam[word]
		else:
			bad_word_occurences = 0

		# Check that it has occured enough times to be informative
		if good_word_occurences + bad_word_occurences >= 5:
			good_rank = min(1.0,2.0*good_word_occurences/ham_file_num)
			bad_rank = min(1.0,1.0*bad_word_occurences/spam_file_num)
			prob = max(0.01, min(0.99, bad_rank/(good_rank+bad_rank)))
			probabilities[word] = prob
	return probabilities

def check_incoming(email_text):
	tokens = re.split("[^a-zA-Z\d\$\'-]", email_text.lower())
	tokens.sort(key=define_interesting)
	tokens = tokens [-15:]
	token_probabilities = [define_interesting(token) for token in tokens]
	token_pi = reduce(operator.mul,token_probabilities)
	conjugate_pi = reduce(operator.mul, [1-token_probability for token_probability in token_probabilities])
	value = token_pi/(token_pi+conjugate_pi)
	return value > 0.9

def define_interesting(word):
	if word not in probability_table:
		return .1
	return abs(.5 - probability_table[word])

def test_file(path):
	file = open(path, "r")
	text = file.read()
	spam_check = check_incoming(text)
	file.close()
	return spam_check


def test_directory(path):
	file_paths = [path + file_name for file_name in os.listdir(path)]
	filtered = 0;
	passed = 0;
	for current_path in file_paths:
		file = open(current_path, "r")
		text = file.read()
		spam_check = check_incoming(text)
		file.close()
		if spam_check:
			filtered += 1
		else:
			passed += 1
	print "Filtered: " + str(filtered) + "\nPassed: " + str(passed)

# Look through spam directories to build hash table of bad words
bad_path1 = 'spam1/'
bad_path2 = 'spam2/'

# Generate the frequency tables for each spam word
spam_dictionary = build_frequency_dictionary(bad_path1)
merge_frequency_dictionaries(spam_dictionary, build_frequency_dictionary(bad_path2))

# Do the same for the ham words, generate the tables
good_path1 = 'easy_ham/'
good_path2 = 'hard_ham/'

ham_dictionary = build_frequency_dictionary(good_path1)
merge_frequency_dictionaries(ham_dictionary, build_frequency_dictionary(good_path2))

# Get the number of spam and ham files
spam_file_num = len(os.listdir(bad_path1)) + len(os.listdir(bad_path2))
ham_file_num = len(os.listdir(good_path1)) + len(os.listdir(good_path2))

# Generate the probabilities table, this is all of the prework that we can do
probability_table = create_probability_table(spam_dictionary, ham_dictionary, spam_file_num, ham_file_num)

single_file = 'spam1/0494.a0865131f55d26362a8efad99c37de01'

print test_file(single_file)


	
