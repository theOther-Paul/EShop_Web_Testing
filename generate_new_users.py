import random
import requests
import json


def get_genders():
    genders = ['Mr.', 'Mrs.']
    return random.choice(genders)


def generate_email():
    pass


def generate_password():
    pass


def generate_first_last_name():
    pass


def user_dump():
    pass


# needs debugging
def api_connection():
    global data
    response = requests.get('https://randomuser.me/api/?inc=gender,name,nat,login')
    if response.status_code == 200:
        print("connection successfully created")
        data = response.json()
        print(data)
        # raw = json.loads(data)
    elif response.status_code == 404:
        print("Unable to reach URL.")
    else:
        print("Unable to connect API or retrieve data.")
    for record in data:
        print(f"Gender: {record['gender']},\n Name : {record['first'] + record['last']}, \n Title : {record['title']}, \n Email : {record['email']}, \nUsername : {record['username']}, \n Password : {record['password']}")


def main():
    api_connection()


if __name__ == '__main__':
    main()
