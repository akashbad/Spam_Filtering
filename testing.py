import os
import spam_filter

# This class is the class you can run from the commandline which will test
# the effectiveness of the spam filter. It can both test how the filter
# responds to a single incident message and how it might respond to a
# directory of files.

# Test a single file to see if it is filtered
def test_file(path):
	file = open(path, "r")
	text = file.read()
	spam_check = spam_filter.check_incoming(text)
	file.close()
	return spam_check

# Test a directory, this can be particularly useful when testing against
# the training data.
def test_directory(path):
	file_paths = [path + file_name for file_name in os.listdir(path)]
	filtered = 0;
	passed = 0;
	for current_path in file_paths:
		file = open(current_path, "r")
		text = file.read()
		spam_check = spam_filter.check_incoming(text)
		file.close()
		if spam_check:
			filtered += 1
		else:
			passed += 1
	return "Filtered: " + str(filtered) + "\nPassed: " + str(passed)

# Paths for spam mail
bad_path1 = 'spam1/'
bad_path2 = 'spam2/'

# Paths for ham mail
good_path1 = 'easy_ham/'
good_path2 = 'hard_ham/'

# Specific test cases I want to check go here

print test_directory(bad_path1)
print test_directory(bad_path2)
print test_directory(good_path1)
print test_directory(good_path2)