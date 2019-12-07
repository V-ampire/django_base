import requests


class Bot(object):
    
    def __init__(self):
        self.session = requests.Session()
        self.users_url = 'https://jsonplaceholder.typicode.com/users'

    def check_users(self):
        users = self.session.get(self.users_url)
        return len(users) == 10

