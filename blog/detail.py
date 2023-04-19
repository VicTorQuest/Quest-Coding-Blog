import os
import requests
from getpass import getpass

auth_endpoint = 'http://127.0.0.1:8000/blogposts/token/'
username = input('Enter your username: ')
password = getpass('Enter your password:')
get_token = requests.post(auth_endpoint, json={'username': username, 'password': password})
print(get_token.text)
print(get_token.status_code)

if get_token.status_code == 200:
    token = get_token.json()['token']

    headers = {
        'Authorization': f'Token {token}'
    }


    endpoint = 'http://127.0.0.1:8000/blogposts/api/'

    get_response = requests.get(endpoint, headers=headers)

    print(get_response.text)
    print(get_response.status_code)
else:
    print('somthing went wrong')