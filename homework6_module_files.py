# Module 6. Module. Files
# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed
# 4.Apply case normalization functionality form Homework 3/4

from datetime import datetime
import sys
import re
import os
from homework4_functions import normalize_text
#import homework5_classesOOP

class NewsFeedTool:
    def __init__(self):
        self.text = input("Enter the message title you would like to add according to chosen type: ")
        self.completed_message = ''
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def create_message_header(self):
        return f"{self.message_name} {(30 - len(self.message_name) - 1) * '-'}"

    def publish_date(self):
        return datetime.today()

    def write_to_file(self):
        with open('newsfeed.txt', 'a') as file:
            file.write(self.completed_message)


class News(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.city = input("Please enter the city: ")
        self.publish_date = self.publish_date().strftime('%d-%m-%Y %H:%M')
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'


class PrivateAd(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.publish_date = self.publish_date()
        self.exp_date = self.expiration_date_validation()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'Actual until: {self.exp_date.date()}, ' \
                                 f'{self.left_days}\n{self.footer}'

    def expiration_date_validation(self):
        exp_date = datetime.strptime(input("Please enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        while exp_date < self.publish_date:
            print("The expiration date can't be less than current date")
            exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        return exp_date


class WeatherCondition(NewsFeedTool):
    def __init__(self):
        super().__init__()
        self.weather_city = input("Please enter the city: ")
        self.weather_condition = input("Please enter the weather condition: ")
        self.temp = self.temp_validation()
        self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                 f'City: {self.weather_city}, ' \
                                 f'Temperature: {self.temp}, ' \
                                 f'How is the weather today?: {self.weather_condition}\n{self.footer}'

    def temp_validation(self):
        temp = input("Please enter the temperature in C (): ")
        while temp.isnumeric() is False:
            print("The temperature could be only numeric value")
            temp = input("Please enter the temperature: ")
        return temp



class TextProcessor:
    #os.getcwd() - current working directory
    def __init__(self, file_to_process, default_folder=os.getcwd(), default_write_file='Newsfeed.txt'):
        self.file_to_process = file_to_process
        self.default_folder = default_folder
        self.default_write_file = default_write_file
        #self.file_to_process = input('Enter your file name to process like "Filename.txt": ')

    def __get_rows_from_file(self):
        source_file_path = os.path(self.file_to_process)
        with open(source_file_path, 'r') as file:
            file_all_content = file.read()
        all_records = re.split('\n\n', file_all_content)
        return all_records

    def write_from_file(self):
        with open(self.default_write_file, 'a') as file:
            for row in self.__get_rows_from_file():
                file.write(row + '\n\n')
        os.remove(os.path(self.file_to_process))


def input_type_validation():
    input_type = int(input('Select input type:\n1 - Input new item\n2 - Process a file\n3 - Exit\n'))
    while input_type not in [1, 2, 3]:
        print("Available options:  1, 2, or 3")
        input_type = int(input('Select input type:\n1 - Input\n2 - Process a file\n3 - Exit\n'))
    return input_type


while True:
    input_type = input_type_validation()
    if input_type == 1:
        input_message_type = input('Please enter the message type that you want to add to the feed '
                                   'or enter "exit" to close the program. '
                                   '\nAvailable message types: News, PrivateAd, Weather: ')
        if input_message_type.lower() == 'exit':
            sys.exit()
        elif input_message_type.lower() == 'news':
            News().write_to_file()
        elif input_message_type.lower() == 'privatead':
            PrivateAd().write_to_file()
        elif input_message_type.lower() == 'weather':
            WeatherCondition().write_to_file()
            print('Not implemented')
    elif input_type == 2:
        user_file = input('Enter the full path to your file like C:\\ : ')
        TextProcessor(file_to_process=user_file).write_from_file()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
