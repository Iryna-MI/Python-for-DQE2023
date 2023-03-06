# Create a tool, which will do user generated news feed:
# 1.User select what data type he wants to add
# 2.Provide record type required data
# 3.Record is published on text file in special format
#
# You need to implement:
# 1.News – text and city as input. Date is calculated during publishing.
# 2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
# 3.Your unique one with unique publish rules.

from datetime import datetime
import sys
import re


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


while True:
    input_message_type = input('\nPlease enter the message type you would like to add to the feed '
                               'or enter "exit" to close the program. '
                               '\n\nAvailable message types: News, PrivateAd, Weather: ')
    if input_message_type.lower() == 'exit':
        sys.exit()
    elif input_message_type.lower() == 'news':
        News().write_to_file()
    elif input_message_type.lower() == 'privatead':
        PrivateAd().write_to_file()
    elif input_message_type.lower() == 'weather':
        WeatherCondition().write_to_file()
    else:
        print('Not implemented')
