#!/usr/bin/env python3
from website import *
import os

def create_users(amount=10):
    for i in range(0, amount):
        username = str(i)
        email = str(i) + '@' + str(i) + '.com'
        password = str(i)

        admin, publisher, moderator = False, False, False
        if i == 0:
            admin, publisher, moderator = True, True, True

        print('Creating user: %s' % str(i))
        print(register(username=username, email=email, password=password,
                 admin=admin, publisher=publisher, moderator=moderator,
                 api=True))
        print()

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