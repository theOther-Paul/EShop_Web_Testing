import requests
import json
from enum import Enum
import os


# will take care of errors and exceptions
class ErrorMessage(Enum):
    API_CONNECTION_ERROR = "Unable to connect to API"
    RETRIEVAL_ERROR = "Unable to retrieve data"
    STORAGE_ERROR = "Function can't save file"


def api_connection():
    response = requests.get('https://randomuser.me/api/?inc=gender,name,nat,login,email')
    if response.status_code == 200:
        data = response.json()
        try:
            with open('api_response/user_data.json', 'w+') as output_data:
                json.dump(data, output_data)
        except ErrorMessage.STORAGE_ERROR:
            return ErrorMessage.STORAGE_ERROR.value
        return data
    elif response.status_code == 404:
        return ErrorMessage.API_CONNECTION_ERROR.value
    else:
        return ErrorMessage.RETRIEVAL_ERROR.value


def get_gender_title(json_file):
    with open(f'api_response/{json_file}') as source:
        data = json.load(source)
        for record in data["results"]:
            return record['name']['title']


def get_email(json_file):
    with open(f'api_response/{json_file}') as source:
        data = json.load(source)
        return ''.join([record['email'] for record in data['results']])


def generate_password(json_file):
    with open(f'api_response/{json_file}') as source:
        data = json.load(source)
        return ''.join([record['login']['password'] for record in data['results']])


def get_first_last_name(json_file):
    with open(f'api_response/{json_file}') as source:
        data = json.load(source)
        return ''.join(record['name']['first'] + ' ' + record['name']['last'] for record in data['results'])


def drop_user_data(json_file):
    os.remove(f'api_response/{json_file}')
