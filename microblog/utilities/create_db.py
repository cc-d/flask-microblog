#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

print(sys.path)

from website import *


def create_users(amount=10, prompt_admin=True):
    users = {}
    for i in range(0, amount):
        # randomly generate 8 character username
        username = random_string(8, uppercase=False)
        # ensure no duplicates
        while username in users.keys():
            username = random_string(8, uppercase=False)

        # ensure half have emails half don't
        if i % 2 == 1:
            email = username + '@' + username + '.com'
        else:
            email = None

        password = username[::-1]

        admin, publisher, moderator = False, False, False
        if i == 0:
            # if admin, 10 character long user and password
            admin, publisher, moderator = True, True, True

            username = random_string(10, uppercase=False)
            password = random_string(10, uppercase=False)

            if prompt_admin:
                prompt = input('Manually enter admin login info? (y/N): ')
                if len(prompt) > 0:
                    if prompt[0].upper() == 'Y':
                        username = input('Enter Admin Username: ')
                        while valid_username(username) is not True:
                            print('Invalid username. Allowed are: A-Z a-z 0-9 -_')
                            username = input('Enter Admin Username: ')

                        password = input('Enter Admin Password (Min 6 Characters): ')
                        while valid_password(password) is not True:
                            print('Invalid password. Must be between 6 and 200 characters.')
                            password = input('Enter Admin Password: ')

                        email = input('Enter Admin Email Address (blank is allowed): ')
                        if email == '':
                            email = None
                        while valid_email(email, allow_empty=True) is not True:
                            print('Invalid email address. Please enter again.')
                            email = input('Enter Admin Email Address (can be blank): ')
                            if email == '':
                                email = None


        print('Creating user: %s' % str(i))
        print(register(username=username, email=email, password=password,
                 admin=admin, publisher=publisher, moderator=moderator,
                 api=True))
        print('\n')

        users[username] = {'email':email, 'password':password, 'admin':admin}

    for u in users.keys():
        if users[u]['admin']:
            print('\n', 30 * '*', '\n')
            print('ADMIN ACCOUNT INFO:\n')
            if users[u]['email'] is not None:
                print('ADMIN EMAIL: ' + users[u]['email'])
            print('ADMIN USERNAME: ' + u)
            print('ADMIN PASSWORD: ' + users[u]['password'])
            print('\n', 30 * '*')

def rebuild_db():
    try:
        os.remove('microblog.db')
    except FileNotFoundError:
        print('SQLITE3 DB does not exist.')

    print('Creating SQLITE3 DB')
    db.create_all()

if __name__ == '__main__':
    rebuild_db()
    create_users()