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
for el in range(random.randint(2, 4)): # random number of dictionaries
    size = random.randint(2, 5)    # random dictionary size
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

# initialize the final and temp dictionary
final_dict, tmp_dict = {},  {}

#Transform from list of dicts into dict of lists.
tmp_dict = {
    k: [d.get(k) for d in dictList] # going through all elements in dictionary list and get values for current key k in current dictionary
    for k in set().union(*dictList) # gets all keys from list of dictionary and unite them distinctly by using set().union to have distinct keys
}

#choose the biggest value
for key, val in tmp_dict.items():
    if int(len(val)) > 1:
        non_none_value = [i for i in val if i is not None]
        max_val = max(non_none_value)
        ind_of_max_val = val.index(max_val)
        if len(non_none_value) > 1:
            final_dict[key+"_"+str(ind_of_max_val+1)] = max_val # max(val))+1 - to identify the # of dictionary with max value
        else: final_dict[key] = max_val
    else:
        final_dict[key] = val[0]

# print result
print("\nTask2. Common dictionary:", final_dict)

