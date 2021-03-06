import config
import re
import os
import json
from time import time
from flask import Flask, Blueprint, render_template, abort, request, g, redirect, flash, url_for, session, send_from_directory
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from models import *
from functions.functions import *

from functions.db_functions import *

cache_bust = '?' + str(time()).replace('.', '')


@app.before_request
def before_request():
    g.cache_bust = cache_bust
    request.show_debug_info = False

    if 'username' in session:
        if 'CSRF_TOKEN' not in session or 'USER_CSRF' not in session:
            session['USER_CSRF'] = random_string(64)
            session['CSRF_TOKEN'] = create_csrf_token(session['USER_CSRF'], config.CSRF_KEY)

    # allows admins to append debug=1 to requests to see debug info
    if 'debug=1' in request.environ['QUERY_STRING'].split('&'):
        if 'admin' in session:
            flash_debug_info()
            request.show_debug_info = True

    if config.DEBUG:
        g.debug_time = time()


@app.after_request
def after_request(response):
    if config.DEBUG:
        print('\n', time() - g.debug_time)

    return response


def clear_csrf_tokens():
    session.pop('USER_CSRF')
    session.pop('CSRF_TOKEN')
    return True

def req_csrf(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST':
            user_csrf = request.form.get('simplecsrf')

            if user_csrf is None:
                flash('no csrf input')
                return logout()

            if user_csrf != session['USER_CSRF']:
                flash('submitted csrf does not match cookie csrf')
                return logout()

            if verify_csrf_token(user_csrf, session['CSRF_TOKEN']) is False:
                flash('submitted csrf does not match combined server & user keys')
                return logout()

            clear_csrf_tokens()
            flash('csrf user token and server token match', 'success')

            return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return decorated


def create_csrf_token(user_token, csrf_key=config.CSRF_KEY):
    from werkzeug.security import generate_password_hash

    token = generate_password_hash(user_token + csrf_key,
                                   method='pbkdf2:sha256:10000',
                                   salt_length=8)
    return token


def verify_csrf_token(user_token, csrf_token, csrf_key=config.CSRF_KEY):
    from werkzeug.security import check_password_hash

    return check_password_hash(csrf_token,
                               user_token + csrf_key)


def simplecsrf():
    return "<input type='hidden' value='%s' name='%s'>" % (session['USER_CSRF'], 'simplecsrf')


app.jinja_env.globals.update(simplecsrf=simplecsrf)


@app.route('/fonts/<file>/')
def font(file=None):
    if os.path.isfile('static/fonts/%s' % file):
        return redirect('/static/fonts/' + file, code=301)
    abort(404)


@app.route('/download/<path:filename>')
def download(filename=None, methods=['GET']):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_PATH'])
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/login', methods=['GET', 'POST'])
def login(useremail=None, password=None):
    useremail = request.form.get('useremail') if useremail is None else useremail
    password = request.form.get('password') if password is None else password

    if request.method == 'GET':
        creating_admin = False

        try:
            # if no user records, prompt admin account creation
            user_count = db.session.query(Buser).first()
            if user_count is None:
                creating_admin = True
        except OperationalError:
            # database does not exist, create it
            db.create_all()
            creating_admin = True

        return render_template('login.html')

    elif request.method == 'POST' or \
            useremail is not None or \
            password is not None:

        if valid_email(useremail):
            user = db.session.query(Buser).filter_by(email=useremail).first()
            login_type = 'email'
        else:
            user = db.session.query(Buser).filter_by(username=useremail).first()
            login_type = 'username'

        if user is None:
            flash('user does not exist', 'danger')
            return redirect(url_for('login'))

        if check_password_hash(user.password, password):
            flash('logged in successfully', 'success')
            session['username'] = user.username
            session['useremail'] = user.email

            if user.admin:
                session['admin'] = True

            return redirect(url_for('blog.blog_index'))
        else:
            flash('invalid password', 'danger')
            return redirect(url_for('login'))


@app.route('/logout/', methods=['GET'])
def logout():
    for key in [k for k in session.keys()]:
        session.pop(key)

    flash('Sucessfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register(username=None, email=None, password=None,
             admin=False, publisher=False, moderator=False, api=False):

    if api is False:
        username = request.form.get('username') if username is None else username
        email = request.form.get('email') if email is None else email
        password = request.form.get('password') if password is None else password

    if valid_username(username) and \
        valid_password(password) and \
            valid_email(email, allow_empty=True):

        is_admin, is_publisher, is_moderator = False, False, False

        # if no other users exist, create this (First) user as an admin
        if db.session.query(Buser).first() is None or admin:
            is_admin, is_publisher, is_moderator = True, True, True

        new_user = Buser(username=username, email=email, admin=is_admin,
                         publisher=is_publisher, moderator=is_moderator,
                         password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        if api:
            juser = {'username':new_user.username, 'email':new_user.email,
                     'password':new_user.password, 'unhashed_pw':password,
                     'admin':new_user.admin, 'publisher':new_user.publisher,
                     'moderator':new_user.moderator}

            return ({'status':'success', 'new_user':juser})

        flash('registered user %s %s %s' % (username, email, password))

        login(useremail=username, password=password)

        return render_template('login.html')

    else:
        abort(500)


from blueprints import user
app.register_blueprint(user.bp)

from blueprints import blog
app.register_blueprint(blog.bp)

from blueprints import admin
app.register_blueprint(admin.bp)