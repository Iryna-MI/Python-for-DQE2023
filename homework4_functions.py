import random
from random import randrange
import string
import re


# create random number of dictionaries
def dicts(num_dicts, values_range):
    dicts_list = []
    for i in range(random.randint(2, num_dicts)):  # random number of dictionaries
        size = random.randint(1, 26)  # random dictionary size = not more than alphabet letters
        keys = random.sample(string.ascii_lowercase, size)  # random letters
        values = (random.randint(1, values_range) for n in range(size))  # random numbers
        mydict = dict(zip(keys, values))  # zip() enable to create dic joining the lists of keys and values
        dicts_list.append(mydict)
    return dicts_list

# create common dictionary
def create_general_dictionary(dict_list):
    # initialize the final and temp dictionary
    final_dict, tmp_dict = {},  {}

    #Transform from list of dicts into dict of lists.
    tmp_dict = {
    k: [d.get(k) for d in dict_list] # going through all elements in dictionary list and get values for current key k in current dictionary
    for k in set().union(*dict_list) # gets all keys from list of dictionary and unite them distinctly by using set().union to have distinct keys
    }

    #choose the biggest value to generate the common dictionary
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
    return final_dict




# normalize text
def normalize_text(start_text):
    # normalize text
    list_of_text = re.split(r'(^|[.])', start_text)

    normalized_text = ''
    for i in list_of_text:
        i = re.sub(r"^\s+", "", i)  # Remove leading space
        i = re.sub(r"\s+$", "", i)  # Remove trailing spaces
        i = re.sub(' +', ' ', i)  # replace more than one whitespace with one whitespace
        normalized_text += i.capitalize()

    # (?<=[.,]) looks for dots or commas
    # (?=[^\s]) look that matches anything that isn't a space
    # add space and go to new line after each sentence
    normalized_text = re.sub(r'(?<=[.])(?=[^\s])', r'\n ', normalized_text)

    # replace misspelling in normalized text
    normalized_text_without_misspelling = normalized_text.replace(' iz ', ' is ')
    return normalized_text_without_misspelling


# create sentence with last words of each existing sentence
def new_sentence(text):
    sentences = [sentence for sentence in text.split('.') if sentence]

    last_sentence = []
    for sentence in sentences:
        last_sentence.append(sentence.split()[-1])
    last_sentence_text = ' '.join(last_sentence) + '.'
    return last_sentence_text.capitalize()

def add_new_sentence(text, last_word_sent):
    to_replace = 'to the end of this paragraph.'
    new_text = text.replace(to_replace, to_replace + '\n' + last_word_sent)
    #new_text = text.replace(where_to_replace,where_to_replace + '\n' + last_word_sent.capitalize())
    #new_text = text.replace(where_to_replace,  where_to_replace + '\n' + text_to_replace)
    return new_text

# calculate number of whitespace character
def whitespaces_culc(text):
    whitespace_characters = len(re.findall(r'\s', text))
    return whitespace_characters


# copy homework text to variable
start_text = """

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# print result lesson3 task1.
# function dicts parameters: 1)num_dicts - range of number of dicts; 2) values_range - range for dicts values
try:
    print("Lesson2.Task1. List of random number of dicts: ", dicts(3, 100))
except:
    print("Something went wrong")

# print result lesson3 task2.
# function create_general_dictionary parameter : list of dictionaries
try:
    dict_list = dicts(3, 100)
    print("Lesson2.Task2. Common dictionary:", create_general_dictionary(dict_list))
except:
    print("Something went wrong")

# print result lesson3 task1: Normalized text
try:
    print('\nLesson3.Task1. Normalized text: \n' + normalize_text(start_text))
except:
    print("Lesson3.Task1. Something happen with text :(")

# print text with new sentence
try:
    old_text = normalize_text(start_text)
    where_to_replace = 'to the end of this paragraph.'
    last_work_sentence = new_sentence(old_text)
    new_text = add_new_sentence(old_text, last_work_sentence)
    print('\n' + "Lesson3.Task2.Text with replaced paragraph: \n", new_text)
except:
    print("Lesson3.Task2: Something went wrong")

# print result lesson3 task3 number of whitespaces
try:
    old_text = normalize_text(start_text)
    print('\n' + 'Lesson3.Task2. Number of whitespace characters: not 87 but', whitespaces_culc(old_text))
except:
    print("lesson3 task3: Something went wrong")