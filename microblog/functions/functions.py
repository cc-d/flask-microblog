import string
import re
import uuid
import random

def valid_username(username=None):
    if username is None:
        return False

    chars = string.ascii_uppercase + string.ascii_lowercase + \
            string.digits + '-_'

    for c in username:
        if c not in chars:
            return False
    return True


def valid_password(password=None):
    if password is None:
        return False

    if type(password) == str:
        if len(password) >= 6 and len(password) <= 200:
            return True
    return False


def valid_email(email=None, allow_empty=False):
    if allow_empty:
        if email is None:
            return True
    else:
        if email is None:
            return False

    if type(email) == str:
        if len(email) > 0 and len(email) < 100:
            m = re.match(r'\S+@\S+\.\S+', email)
            if m is None:
                return False
            else:
                if m[0] == email:
                    return True
    return False


def gen_invite_link():
    return str(uuid.uuid4())


def random_string(length1, length2=None,
                  lowercase=True, uppercase=True,
                  digits=True, special=False):
    char_pool = ''
    char_pool = char_pool + string.ascii_lowercase if lowercase else char_pool
    char_pool = char_pool + string.ascii_uppercase if uppercase else char_pool
    char_pool = char_pool + string.digits if digits else char_pool
    char_pool = char_pool + '_-' if special else char_pool

    if length2 is not None:
        if length2 > length1:
            ran_len = random.choice([x for x in range(length1, length2)])
        else:
            ran_len = random.choice([x for x in range(length2, length1)])
        return ''.join([random.choice(char_pool) for x in range(0, ran_len)])
    else:
        return ''.join([random.choice(char_pool) for x in range(0, length1)])

