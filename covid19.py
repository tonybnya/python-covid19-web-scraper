#!/usr/bin/env python3

'''
covid19_web_scraper.py      : python program to scrape covid19 data.
Link to the site            : https://www.worldometers.info/coronavirus/
App using for scraping      : ParseHub (https://www.parsehub.com/)
'''

import json
import sys
import time
import requests
import colorama
from colorama import Fore, Style
from progress.bar import FillingSquaresBar, FillingCirclesBar

colorama.init(autoreset=True)

'''
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL.
'''


API_KEY = 'your_api_key'
PROJECT_TOKEN = 'your_project_token'
RUN_TOKEN = 'your_run_token'


class Data:
    '''
    A class defined to scrape data from worldometer with ParseHub App.
    '''

    def __init__(self, api_key, project_token):
        '''Initialize attributes for the class Data.'''

        self.api_key = api_key
        self.project_token = project_token
        self.params = {'api_key': self.api_key}
        self.get_data()

    def get_data(self):
        '''Method to scrape data with the construted API.'''

        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={'api_key': API_KEY})
        self.data = json.loads(response.text)


def get_world_data():
    '''Function to get world wide data.'''

    data = Data(API_KEY, PROJECT_TOKEN)
    now = time.ctime()
    separator = Fore.CYAN + '+' + '-' * 70 + '+'
    heading = f'COVID-19 CORONAVIRUS PANDEMIC {Style.BRIGHT}{Fore.CYAN}(WORLD WIDE DATA)'

    pop = 0
    number = 0
    lst = data.data['country']
    for content in lst:
        try:
            number = content['population'].replace(',', '')
        except KeyError:
            # Failing Silently
            pass
        else:
            pop += int(number)

    print(separator)
    print(f'{Fore.CYAN}|{Fore.RESET}\t {heading}')
    print(f'{Fore.CYAN}|{Fore.RESET}\t Last Update: {now}')
    print(separator)

    progress_bar = FillingSquaresBar(f'{Fore.CYAN}|{Fore.RESET}\t Getting Data...')
    for i in range(100):
        time.sleep(.02)
        progress_bar.next()
    progress_bar.finish()

    print(separator)
    my_dict = data.data

    cases = my_dict['total'][0]['name']
    cases_value = my_dict['total'][0]['value']

    deaths = my_dict['total'][1]['name']
    deaths_value = my_dict['total'][1]['value']

    recovered = my_dict['total'][2]['name']
    recovered_value = my_dict['total'][2]['value']

    print(f"{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}World's Population: {pop:,d}")
    print(f'{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}{cases} {Fore.YELLOW}{cases_value}')
    print(f'{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}{recovered} {Fore.GREEN}{recovered_value}')

    cases_value = int(cases_value.replace(',', ''))

    recovered_value = int(recovered_value.replace(',', ''))
    cure_rate = (recovered_value / cases_value) * 100
    print(f'{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}Cure Rate: {Fore.GREEN}{round(cure_rate, 2)} %')

    print(f'{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}{deaths} {Fore.RED}{deaths_value}')

    deaths_value = int(deaths_value.replace(',', ''))
    death_rate = (deaths_value / cases_value) * 100
    print(f'{Fore.CYAN}|{Fore.RESET}\t {Style.BRIGHT}Death Rate: {Fore.RED}{round(death_rate, 2)} %')

    print(separator)
    link = 'https://www.worldometers.info/coronavirus/'
    print(f'{Fore.CYAN}|{Fore.RESET}\t Source: {link}')
    print(separator)


def get_country_data(country):
    '''Function to get data for a given & valid country name.'''

    data = Data(API_KEY, PROJECT_TOKEN)
    now = time.ctime()
    separator = Fore.BLUE + '+' + '-' * 70 + '+'
    heading = f'COVID-19 CORONAVIRUS PANDEMIC {Style.BRIGHT}{Fore.CYAN}({country.upper()} DATA)'

    print(separator)
    print(f'{Fore.BLUE}|{Fore.RESET}\t {heading}')
    print(f'{Fore.BLUE}|{Fore.RESET}\t Last Update: {now}')
    print(separator)

    progress_bar = FillingCirclesBar(f'{Fore.BLUE}|{Fore.RESET}\t Getting Data...')
    for i in range(100):
        time.sleep(.02)
        progress_bar.next()
    progress_bar.finish()

    print(separator)
    lst = data.data['country']
    my_dict = {}
    for content in lst:
        if content['name'].lower() == country.lower():
            my_dict = content
            print(f"{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Country: {my_dict['name']}")
            print(f"{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Population: {my_dict['population']}")
            print(f"{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Total Cases: {Fore.YELLOW}{my_dict['total_cases']}")
            print(f"{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Total Recovered: {Fore.GREEN}{my_dict['total_recovered']}")

            total_cases = int(content['total_cases'].replace(',', ''))
            total_deaths = int(content['total_deaths'].replace(',', ''))
            total_recovered = int(content['total_recovered'].replace(',', ''))

            cure_rate = (total_recovered / total_cases) * 100
            print(f'{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Cure Rate: {Fore.GREEN}{round(cure_rate, 2)} %')

            print(f"{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Total Deaths: {Fore.RED}{my_dict['total_deaths']}")

            death_rate = (total_deaths / total_cases) * 100
            print(f'{Fore.BLUE}|{Fore.RESET}\t {Style.BRIGHT}Death Rate: {Fore.RED}{round(death_rate, 2)} %')

            print(separator)
            link = 'https://www.worldometers.info/coronavirus/'
            print(f'{Fore.BLUE}|{Fore.RESET}\t Source: {link}')
            print(separator)


def main():
    '''Main program.'''

    if len(sys.argv) != 2:
        print('Usage: ./covid19.py [--global | --country]')
        sys.exit(1)

    option = sys.argv[1]
    if option == '--global':
        print()
        get_world_data()
        print()
    elif option == '--country':
        country = input('Enter a country name: > ')
        get_country_data(country)
        print()
    else:
        print(f"Unknown option: '{option}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
