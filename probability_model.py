import os
import re


# This class is responsible for looking at the training data and building a
# probabality table to represent the occurence of tokens through the training
# set. 

# The set of paths from the root directory where the training data is loaded
# for now this is hard coded but could be modified to take the path as an input

# Paths for spam mail
bad_path1 = 'spam1/'
bad_path2 = 'spam2/'

# Paths for ham mail
good_path1 = 'easy_ham/'
good_path2 = 'hard_ham/'

# This is the top level static function which will call all other functions to
# look through training data and generate the probability table
def establish_model():
	# Build the frequency table for the spam set of training data
	spam_dictionary = build_frequency_dictionary(bad_path1)
	merge_frequency_dictionaries(spam_dictionary, build_frequency_dictionary(bad_path2))

	# Build the frequency table for the ham set of training data
	ham_dictionary = build_frequency_dictionary(good_path1)
	merge_frequency_dictionaries(ham_dictionary, build_frequency_dictionary(good_path2))

	# Record the total spam and ham files trained upon
	spam_file_num = len(os.listdir(bad_path1)) + len(os.listdir(bad_path2))
	ham_file_num = len(os.listdir(good_path1)) + len(os.listdir(good_path2))

	# Generate the probabilities table using the frequency data and the number of files 
	# trained upon
	return create_probability_table(spam_dictionary, ham_dictionary, spam_file_num, ham_file_num)


# The following functions are all of the internal functions which are called
# to generate the probability table

# This function takes a dictionary address and builds a 
# frequency table of all of the words in all of the files
def build_frequency_dictionary(path):
	file_paths = [path + file_name for file_name in os.listdir(path)]
	words = []
	for current_path in file_paths:
		# Get the text from files and split by non-word characters
		file = open(current_path, "r")
		text = file.read()
		x = re.split("[^a-zA-Z\d\$\'-]", text.lower())
		words.extend(x)
		file.close()
	# Filter out all numbers and blanks
	words = filter(lambda a: a != '' and not a.isdigit(),words)
	frequency_dictionary = {}
	# Establish the frequency table
	for word in words:
		try:
			frequency_dictionary[word] += 1
		except:
			frequency_dictionary[word] = 1
	return frequency_dictionary

# This function merges two frequency tables by adding together the frequencies
# of identical items
def merge_frequency_dictionaries(target_dictionary, other_dictionary):
	for word in other_dictionary.keys():
		if target_dictionary.has_key(word):
			target_dictionary[word] += other_dictionary[word]
		else:
			target_dictionary[word] = other_dictionary[word]

# This function is used to create the probability table using
# the spam and ham traning data and the number of files each
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
			# Apply the appropriate function to establish the probabilities
			good_rank = min(1.0,2.0*good_word_occurences/ham_file_num)
			bad_rank = min(1.0,1.0*bad_word_occurences/spam_file_num)
			prob = max(0.01, min(0.99, bad_rank/(good_rank+bad_rank)))
			probabilities[word] = prob
	return probabilities




	
