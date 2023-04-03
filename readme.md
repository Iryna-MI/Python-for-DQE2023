 # tool, which allows user generated news feed:
# 1.User is able to select what type of message she/he would like to add.
# Possible ways to add new items:
#- input
#- provide records by file: txt, json, xml
# 2.Records are published to the text file in special format.
# 3.Input file will be removed if all records are successfully processed.
# 4. There is a possibility to enter number of records to process (except xml:), xml - is fully processed
#
# Default values:
# if user folder and file were not provided default folder and file are used.
# By default file type is txt.
# By default records count = 1
#
# Message types
# 1. News – text and city as input. Date is calculated during publishing.
# 2. Privatead – text and expiration date as input. Day left is calculated during publishing.
# 3. Weather - city, temperature and weather condition
#
# Result Files:
# 1. csv result files:
#https://github.com/Iryna-MI/Python-for-DQE2023/blob/main/letters_counts.csv
#https://github.com/Iryna-MI/Python-for-DQE2023/blob/main/words_counts.csv
# 2. newsfeed.txt - result file with messages