from blog import app as app
from blog import db as db

class Buser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Buser %r>' % self.username

class Invite_link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(100), unique=True, nullable=True)
    created_by = db.Column(db.String(20), db.ForeignKey('buser.username'), nullable=False)
    used_by = db.Column(db.String(20), db.ForeignKey('buser.username'), default=None)

    def __repr__(self):
        return '<Invite %r>' % self.id