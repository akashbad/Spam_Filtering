import os
import re

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


# Look through spam directories to build hash table of bad words
bad_path1 = 'spam1/'
bad_path2 = 'spam2/'

spam_dictionary = build_frequency_dictionary(bad_path1)
merge_frequency_dictionaries(spam_dictionary, build_frequency_dictionary(bad_path2))

good_path1 = 'easy_ham/'
good_path2 = 'hard_ham/'

ham_dictionary = build_frequency_dictionary(good_path1)
merge_frequency_dictionaries(ham_dictionary, build_frequency_dictionary(good_path2))

spam_file_num = len(os.listdir(bad_path1)) + len(os.listdir(bad_path2))
ham_file_num = len(os.listdir(good_path1)) + len(os.listdir(good_path2))

probabilities = create_probability_table(spam_dictionary, ham_dictionary, spam_file_num, ham_file_num)

print probabilities


	
