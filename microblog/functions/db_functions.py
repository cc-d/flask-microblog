import sys
sys.path.append('..')

from website import *


def normalize_username(username=None):
    if username is not None:
        username = db.session.query(Buser.username).filter(
            func.lower(Buser.username) == func.lower(username)
        ).first()
        if username is None:
            return None
        if len(username) > 0:
            username = username[0]
    return username


def is_admin(username=None):
    if username is not None:
        user = db.session.query(Buser.admin).filter_by(
            username=normalize_username(username)
        ).first()
        if user is None:
            return False
        if len(user) > 0:
            return user[0]
    return False


def flash_debug_info():
    if 'admin' in session:
        if session['admin'] is True:
            k = session.keys()
            k2 = [session[i] for i in k]

            flash(k)
            flash(k2)
            flash(str(vars(request)))
    return True
