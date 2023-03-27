# Expand previous Homework 5/6/7 with additional class, which allow to provide records by JSON file:
#
# 1.Define your input format (one or many records)
#
# 2.Default folder or user provided file path
#
# 3.Remove file if it was successfully processed

from datetime import datetime
import sys
import re
import os
import json
from homework4_functions import normalize_text
import homework7_csv


class NewsFeedTool:
    def __init__(self):
        self.text = input("Enter the message title you would like to add according to chosen type: ")
        self.completed_message = ''
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def create_message_header(self):
        return f"{self.message_name} {(30 - len(self.message_name) - 1) * '-'}"

    def _init_formatting_data(self):
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def publish_date(self):
        return datetime.today()

    def write_to_file(self):
        with open('newsfeed.txt', 'a') as file:
            file.write(self.completed_message)


class News(NewsFeedTool):
    def __init__(self, text='', city='', publish_date=None, is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.city = input("Enter the city name: ")
            self.publish_date = self.publish_date().strftime('%d-%m-%Y %H:%M')
        else:
            self.text = text
            self.city = city
            self.publish_date = publish_date
            super()._init_formatting_data()
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'


class PrivateAd(NewsFeedTool):
    def __init__(self, text='', exp_date=None, is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.publish_date = self.publish_date()
            self.exp_date = self.expiration_date_validation()
        else:
            self.text = text
            self.exp_date = datetime.strptime(exp_date, '%d-%m-%Y')
            self.publish_date = self.publish_date()
            super()._init_formatting_data()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'Actual until: {self.exp_date.date()}, ' \
                                 f'{self.left_days}\n{self.footer}'

    def expiration_date_validation(self):
        #exp_date = datetime.strptime(input("Please enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        try:
            exp_date = datetime.strptime(input("Please enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
            re.match("^([0-9]{2})-([0-9]{2})-([0-9]{4})$", exp_date)
        except ValueError as err:
            print("Error. Enter date in format dd-mm-yyyy")
            exp_date = datetime.strptime(input("\nPlease enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        while exp_date < self.publish_date:
            print("The expiration date can't be less than current date")
            exp_date = datetime.strptime(input("Enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
        return exp_date


class WeatherCondition(NewsFeedTool):
    def __init__(self, weather_city='', weather_condition='', temp='', is_manual=1):
        if is_manual == 1:
            super().__init__()
            self.weather_city = input("Please enter the city: ")
            self.weather_condition = input("Please enter the weather condition: ")
            self.temp = self.temp_validation()
            self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                     f'City: {self.weather_city}, ' \
                                     f'Temperature: {self.temp}, ' \
                                     f'How is the weather today?: {self.weather_condition}\n{self.footer}'
        else:
            self.weather_city = weather_city
            self.weather_condition = weather_condition
            self.temp = temp
            super()._init_formatting_data()
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


class FileProcessor:
    #def __init__(self, default_folder=os.getcwd(), default_write_file='Newsfeed.txt'):
        #self.rows_to_process = int(input('Enter how many records to process: '))
        #self.default_folder = default_folder
        #self.default_write_file = default_write_file
        #self.file_to_process = input('Enter your file name to process like "FileName.FileFormat": ')
    def __init__(self, file_folder, file_to_process, default_folder=os.getcwd(), default_write_file='Newsfeed.txt'):
        self.rows_to_process = int(input('Enter how many records to process: '))
        self.file_folder = file_folder
        self.file_to_process = file_to_process
        self.default_folder = default_folder
        self.default_write_file = default_write_file


class JsonProcessor(FileProcessor):
    def __init__(self, file_folder, file_to_process, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__(file_folder, file_to_process)

    def __get_rows_from_file(self):
        json_data = {}
        source_file_path = os.path.join(self.file_folder, self.file_to_process)
        with open(source_file_path, 'r') as json_file:
            raw_json_data = json.load(json_file)
        counter = self.rows_to_process
        for key, value in raw_json_data.items():
            json_data.update({key: value})
            counter -= 1
            #raw_json_data.pop(key)
            if counter == 0:
                break
        return json_data

    def write_from_file(self):
        json_to_process = self.__get_rows_from_file()
        for newsfeed in json_to_process.values():
            if newsfeed['msg_type'] == 'news':
                News(newsfeed['text'], newsfeed['city'], newsfeed['publish_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'privatead':
                PrivateAd(newsfeed['text'], newsfeed['exp_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'WeatherCondition':
                WeatherCondition(newsfeed['weather_city'], newsfeed['weather_condition'], newsfeed['temp'], is_manual=0).write_to_file()
            else:
                print('Message type not implemented')


class TextProcessor(FileProcessor):
    def __init__(self, file_folder, file_to_process, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__(file_folder, file_to_process)

    def __get_rows_from_file(self):
        source_file_path = os.path.join(self.file_folder, self.file_to_process)
        with open(source_file_path, 'r') as file:
            file_all_content = file.read()
        list_of_records = re.split('\n\n', file_all_content)
        # number of rows to process
        return list_of_records[0:self.rows_to_process]

    def check_file(self):
        source_file_path = os.path.join(self.file_folder, self.file_to_process)
        match = True
        pattern = ['New', 'Ad', 'Weather']
        with open(source_file_path, 'r') as file:
            content = file.read()
            # Iterate list to find each word
            for word in pattern:
                if word in content:
                    match = True
                else:
                    match = False
        return match

    def write_from_file(self):
        if self.check_file():
            with open(self.default_write_file, 'a') as file:
                for row in self.__get_rows_from_file():
                    file.write(row + '\n\n')
        else:
            print("Correct file not found")
            # If file exists, delete it./delete row from file
            source_file_path = os.path.join(self.file_folder, self.file_to_process)
        #if os.path.isfile(source_file_path):
            #os.remove(source_file_path)
        #else:
            ## If it fails, inform the user.
            #print("Error: %s file not found" % source_file_path)


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
            homework7_csv.CsvStatisticsCalculator('Newsfeed.txt').run_statistics()
        elif input_message_type.lower() == 'privatead':
            PrivateAd().write_to_file()
            homework7_csv.CsvStatisticsCalculator('Newsfeed.txt').run_statistics()
        elif input_message_type.lower() == 'weather':
            WeatherCondition().write_to_file()
            homework7_csv.CsvStatisticsCalculator('Newsfeed.txt').run_statistics()
        else:
            print('Not implemented')
    elif input_type == 2:
        file_type = int(input('Please select which type of the file you want to process:'
                                     '\n1 - Txt File\n2 - Json file\n'))
        folder_choose = int(input('Select folder path type to file location:\n1 - Default Folder\n'
                                  '2 - User folder\n'))
        user_file_path = input('Enter the full path to your file like C:\\ : ')
        file_name = input('Enter file name to process like "Name.txt": ')
        if user_file_path and file_name:
            if file_type == 1:
                TextProcessor(file_folder=user_file_path, file_to_process=file_name, ).write_from_file()
            else:
                JsonProcessor(file_folder=user_file_path, file_to_process=file_name, ).write_from_file()
        if not user_file_path:
            user_file_path = os.getcwd()
            default_write_file = 'testfeed.txt'
            if file_type == 1:
                TextProcessor(file_folder=user_file_path, file_to_process=default_write_file, ).write_from_file()
            else:
                JsonProcessor(file_folder=user_file_path, file_to_process=file_name, ).write_from_file()
        homework7_csv.CsvStatisticsCalculator('Newsfeed.txt').run_statistics()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
