import os
import requests
from datetime import datetime

from .constants import Constants


def download(day_number: int):
    now = datetime.now()
    if now < datetime(Constants.YEAR, Constants.MONTH, day_number):
        raise Exception(f'Too early to download day {day_number}')
    try:
        filename = os.path.join('inputs', f'd{day_number:0>2}.in')
        if not os.path.exists('inputs'):
            os.mkdir('inputs')
        if os.path.exists(filename):
            _print_file(filename)
            print(f'File {filename} exists')
        else:
            response = requests.get(
                f'{Constants.URL}/day/{day_number}/input',
                headers={
                    'User-Agent': Constants.USER_AGENT
                },
                cookies={
                    'session': os.getenv('AOC_SESSION_2023')
                }
            )

            if not response.ok:
                print(f'Error in retrieving input: Code {response.status_code}')
                match response.status_code:
                    case 400: print(f'Try resetting session cookie')
                    case 404: print(f'Too soon, try again later')
                response.raise_for_status()

            _create_file(filename, response.text)
            _print_file(filename)
            print(f'File saved as {filename}')

    except KeyError as e:
        print(f'Missing environment variable {e}')
        raise


def _create_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def _print_file(filename):
    with open(filename) as f:
        print(f.read())
