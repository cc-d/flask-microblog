import config
import re
import os
from time import time
from flask import Flask, Blueprint, render_template, abort, request, g, redirect, flash, url_for, session
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


@app.route('/fonts/<file>')
def font(file=None):
    if os.path.isfile('static/fonts/%s' % file):
        return redirect('/static/fonts/' + file, code=301)
    abort(404)


@app.route('/')
def index():
    return render_template('index.html')


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

        return render_template('login.html', creating_admin=creating_admin)

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

            return redirect(url_for('index'))
        else:
            flash('invalid password', 'danger')
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Sucessfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register(username=None, email=None, password=None):
    username = request.form.get('username') if username is None else username
    email = request.form.get('email') if email is None else email
    password = request.form.get('password') if password is None else password

    if valid_username(username) and \
        valid_password(password) and \
            valid_email(email):

        is_admin = False
        if db.session.query(Buser).first() is None:
            is_admin = True

        new_user = Buser(username=username, email=email, admin=is_admin,
                         password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        flash('registered user %s %s %s' % (username, email, password))

        login(useremail=username, password=password)

        return render_template('login.html')

    else:
        abort(500)

from blueprints import user
app.register_blueprint(user.bp)