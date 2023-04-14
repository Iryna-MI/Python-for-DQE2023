# Module 10. Database API
# Expand previous Homework 5/6/7/8/9 with additional class, which allow to save records into database:
# 1.Different types of records require different data tables
# 2.New record creates new row in data table
# 3.Implement “no duplicate” check.

from datetime import datetime
import sys
import re
import os
import json
from homework4_functions import normalize_text
import homework7_csv
import xml.etree.ElementTree as ElementTree
import sqlite3

class MyDB:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = sqlite3.connect(self.database_url)
        self.cursor = self.connection.cursor()
        #self.cursor.execute("DROP TABLE tblNews;")

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tblNews(Message VARCHAR(250), City VARCHAR(250), PublishDate DATETIME)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tblPrivatead(Message VARCHAR(250), ExpirationDate DATETIME, PublishDate DATE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tblWeather(City VARCHAR(250), Weather_condition VARCHAR(250), Temperature INT)''')

    def insert_row(self, table_name, datadict):
        columns = [key for key in datadict.keys()]
        values = [f"'{datadict[col]}'" for col in columns]
        query = f"INSERT INTO {table_name}({', '.join(columns)}) values ({', '.join(values)});"
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def check_no_duplicate (self, table_name, datadict):
        param = ' AND '.join([f"{key} = '{datadict[key]}'" for key in datadict.keys()])
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {param};"
        self.cursor.execute(query)
        return int(self.cursor.fetchone()[0]) > 0

    def process_into_db (self, table_name, datadict):
        self.create_tables()
        if not self.check_no_duplicate(table_name, datadict):
            self.insert_row(table_name, datadict)
            print(f'Row was inserted into  {table_name} table into database.')
        else:
            print(f'DUPLICATE. Row was NOT inserted into database table {table_name}.')

class NewsFeedTool:
    def __init__(self):
        self.text = input("Enter the message title you would like to add according to chosen type: ")
        self.completed_message = ''
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'
        self._init_db_data()

    def create_message_header(self):
        return f"{self.message_name} {(30 - len(self.message_name) - 1) * '-'}"

    def _init_formatting_data(self):
        self.message_name = ' '.join(re.findall('[A-Z][^A-Z]*', self.__class__.__name__))
        self.header = self.create_message_header()
        self.footer = 30 * '-' + '\n\n'

    def _init_db_data(self):
        self.conn = MyDB('newsfeed.db')
        self.table_name = ''
        self.content_db = dict()

    def publish_date(self):
        return datetime.today()

    def write_to_file(self):
        with open('newsfeed.txt', 'a') as file:
            file.write(self.completed_message)
        self.conn.process_into_db(self.table_name, self.content_db)



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
            super()._init_db_data()
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'{self.city.capitalize()}, {self.publish_date}\n' \
                                 f'{self.footer}'
        self.table_name = 'tblNews'
        self.table_content = {'Message': normalize_text(self.text), 'City': self.city.capitalize(),
                              'PublishDate': self.publish_date}
        self.content_db = self.table_content


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
            super()._init_db_data()
        self.left_days = f'{(self.exp_date - self.publish_date).days + 1} days left'
        self.completed_message = f'{self.header}\n{normalize_text(self.text)}\n' \
                                 f'Actual until: {self.exp_date.date()}, ' \
                                 f'{self.left_days}\n{self.footer}'
        self.table_name = 'tblPrivatead'
        self.content_db = {'Message': normalize_text(self.text), 'ExpirationDate': self.exp_date.date(),
                           'PublishDate': self.publish_date.strftime('%d-%m-%Y %H:%M')}

    def expiration_date_validation(self):
        exp_date = datetime.strptime(input("Please enter the expiration date (dd-mm-yyyy): "), '%d-%m-%Y')
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
            super()._init_db_data()
            self.completed_message = f'{self.header}\n{self.text.capitalize()}\n' \
                                     f'City: {self.weather_city}, ' \
                                     f'Temperature: {self.temp}, ' \
                                     f'How is the weather today?: {self.weather_condition}\n{self.footer}'
        self.table_name = 'tblWeather'
        self.content_db = {'City': normalize_text(self.weather_city),
                               'Weather_condition': normalize_text(self.weather_condition),
                               'Temperature': self.temp}

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
        user_input = input('Enter how many records to process(!!! XML will be fully processed): ')
        try:
            self.rows_to_process = int(user_input)
        except ValueError:
            self.rows_to_process = 1
        self.file_folder = file_folder
        self.file_to_process = file_to_process
        self.default_folder = default_folder
        self.default_write_file = default_write_file


class XmlProcessor(FileProcessor):
    def __init__(self, file_folder, file_to_process, default_folder=None):
        if default_folder:
            super().__init__(default_folder)
        else:
            super().__init__(file_folder, file_to_process)

    def __get_rows_from_file(self):
        xml_file = ElementTree.parse(os.path.join(self.file_folder, self.file_to_process))
        xml_root = xml_file.getroot()
        xml_messages = []
        #counter = self.rows_to_process
        for elements in xml_root:
            temp_dict = {}
            for tag in elements:
                temp_dict[tag.tag] = tag.text
            xml_messages.append(temp_dict)
            #counter -= 1
            #if counter == 0:
                #break
        return xml_messages

    def write_from_file(self):
        xml_to_process = self.__get_rows_from_file()
        for newsfeed in xml_to_process:
            if newsfeed['msg_type'] == 'news':
                News(newsfeed['text'], newsfeed['city'], newsfeed['publish_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'privatead':
                PrivateAd(newsfeed['text'], newsfeed['exp_date'], is_manual=0).write_to_file()
            elif newsfeed['msg_type'] == 'WeatherCondition':
                WeatherCondition(newsfeed['weather_city'], newsfeed['weather_condition'], newsfeed['temp'],
                                 is_manual=0).write_to_file()
            else:
                print('Message type not implemented')
        os.remove(os.path.join(self.file_folder, self.file_to_process))


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
            #delete processed rows
            del raw_json_data[key]
            if counter == 0:
                break
        with open(source_file_path, 'w') as f:
            f.write(json.dumps(raw_json_data, indent=2))

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
        return list_of_records[0:]

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
        records = []
        records = self.__get_rows_from_file()
        if self.check_file():
            with open(self.default_write_file, 'a') as file:
                counter = self.rows_to_process
                for row in self.__get_rows_from_file():
                    file.write(row + '\n\n')
                    records.remove(row)
                    counter -= 1
                    if counter == 0:
                        break
            source_file_path = os.path.join(self.file_folder, self.file_to_process)
            with open(source_file_path, 'w') as f:
                for r in records:
                    f.write(r)
        else:
            print("Correct file not found")
            # If file exists, delete it./delete row from file
            source_file_path = os.path.join(self.file_folder, self.file_to_process)
        #if os.path.isfile(source_file_path):
        if os.stat(source_file_path).st_size == 0:
            os.remove(source_file_path)


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
                                     '\n1 - Txt File\n2 - Json file\n3 - XML file\n'))
        folder_choose = int(input('Select folder path type to file location:\n1 - Default Folder\n'
                                  '2 - User folder\n'))
        user_file_path = input('Enter the full path to your file like C:\\ : ')
        file_name = input('Enter file name to process like "Name.format": ')
        user_file_path = user_file_path or os.getcwd()
        #if user_file_path and file_name:
        if file_type == 1:
            TextProcessor(file_folder=user_file_path, file_to_process=file_name or 'testfeed.txt', ).write_from_file()
        elif file_type == 2:
            JsonProcessor(file_folder=user_file_path, file_to_process=file_name or 'testfeed.json', ).write_from_file()
        elif file_type == 3:
                XmlProcessor(file_folder=user_file_path, file_to_process=file_name or 'testfeed.xml', ).write_from_file()
        else:
            print ("File type not supported")
        homework7_csv.CsvStatisticsCalculator('Newsfeed.txt').run_statistics()
    elif input_type == 3:
        sys.exit()
    else:
        print('Not implemented')
