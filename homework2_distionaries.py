# Module 2. Collections

# Task 1. Create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
import string
import random

# Task 1. create a list of random number of dicts (from 2 to 10)

# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

dictList = []
for el in range(random.randint(2, 10)): # random number of dictionaries
    size = random.randint(2, 10)    # random dictionary size
    keys = random.sample(string.ascii_lowercase, size)  # random letters for dictionaries keys
    values = (random.randint(0, 100) for val in range(size)) # random numbers
    #The zip(fields, values) method returns an iterator that generates two-items tuples.
    # If call dict() on that iterator, dictionary can be created that is needed.
    # The elements of the first list become the dictionary’s keys, and the second list represents the values in the dictionary.
    myDict = dict(zip(keys, values))                      # create a dictionary
    dictList.append(myDict)                              # add it to the list

print("\nTask 1. List of random number of dictionaries: " + str(dictList))

# Task 2. Get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

# initialize the final dictionary
final_dict, tmp_dict= {},  {}

#Transform from list of dicts into dict of lists.
for dictionary in dictList:
  for key, val in dictionary.items():
      # returns the key value available in the dictionary
      # and if given key is not available then it will return provided default value, value that was chosen
      # add all found values for the chosen key
      # setdefault returns the list
    tmp_dict.setdefault(key, []).append(val)

#choose the biggest value
for key, val in tmp_dict.items():
    if len(val) > 1:
        final_dict[key+"_"+str(val.index(max(val))+1)] = max(val) # max(val))+1 - to identify the # of dictionary with max value
    else: final_dict[key] = val[0]

# print result
print("\nTask2. Common dictionary:", final_dict)