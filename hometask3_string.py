# Module 3. String Object

import re

# copy homework text to variable
start_text = """
  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# normalize text
list_of_text = re.split(r'(^|[.])', start_text)

normalized_text = ''
for i in list_of_text:
    i = re.sub(r"^\s+", "", i) #Remove leading space
    i = re.sub(r"\s+$", "", i) #Remove trailing spaces
    i = re.sub(' +', ' ', i) #replace more than one whitespace with one whitespace
    normalized_text += i.capitalize()

#(?<=[.]) search for dots 
#(?=[^\s]) look that matches anything that isn't a space
#add space and go to new line after each sentence
normalized_text = re.sub(r'(?<=[.])(?=[^\s])', r'\n ', normalized_text)

# replace misspelling in normalized text
normalized_text_without_misspelling = normalized_text.replace(' iz ', ' is ')

# create sentence with last words of each existing sentence
sentences = [sentence for sentence in normalized_text_without_misspelling.split('.') if sentence]

last_sentence = []
for sentence in sentences:
    last_sentence.append(sentence.split()[-1])
last_sentence_text = ' '.join(last_sentence) + '.'

#add new sentence to the END OF this Paragraph.
to_replace = 'add it to the end of this paragraph.'
normalized_text_without_misspelling = normalized_text_without_misspelling.replace(to_replace, to_replace + '\n'+ last_sentence_text.capitalize())

print("\n********* Normalized text ******************\n", normalized_text_without_misspelling)

# calculate number of whitespace character
whitespace_characters = len(re.findall(r'\s', start_text))

print('\n' + 'Number of whitespace characters #1: ', whitespace_characters)

