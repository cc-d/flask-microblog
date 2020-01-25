import string
import re
import uuid

def valid_username(username=None):
    print(username)
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
        if len(password) > 0 and len(password) < 200:
            return True
    return False

def valid_email(email=None):
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