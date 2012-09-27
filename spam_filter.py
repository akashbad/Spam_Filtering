import os
import re

# Look through spam directories to build hash table of bad words
bad_path1 = 'spam1/'
bad_path2 = 'spam2/'


# Internal functions, used to build dictionaries of spam data
def build_frequency_dictionary(path):
	file_paths = [path + file_name for file_name in os.listdir(path)]
	words = []
	for current_path in file_paths:
		file = open(current_path, "r")
		text = file.read()
		x = re.split("[^a-zA-Z\d\$\'-]", text)
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




	
