from website import app as app
from website import db as db

from markdown import markdown


class Buser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    moderator = db.Column(db.Boolean, default=False, nullable=False)
    publisher = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Buser %r>' % self.username


class Blog(db.Model):
    from datetime import datetime
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), db.ForeignKey('buser.username'), default=None)
    title = db.Column(db.String(200), default='Untitled', nullable=False)
    text = db.Column(db.String(100000), default=None)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    edited = db.Column(db.DateTime, default=None)
    custom_url = db.Column(db.String(200), default=None)

    # public, private, unpublished
    visibility = db.Column(db.String(20), default='public', nullable=False)

    def __repr__(self):
        return '<Blog %r>' % self.id

    def markdown_text(self):
        return markdown(self.text)
