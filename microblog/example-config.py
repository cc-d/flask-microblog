# Always should be False in PROD
DEBUG = True

# Base url, self-explanatory
URL = 'http://107.161.20.20:10000'

# change to decent large random string
SECRET_KEY = 'changeme'

# performance improvement
SQLALCHEMY_TRACK_MODIFICATIONS = False

# choose to use either postgresql or sqlite3, both work
#DB_TYPE = 'sqltie3'
DB_TYPE = 'sqlite'

DB_NAME = 'microblog'

if DB_TYPE == 'postgres':
    PG_USER = 'test'
    PG_PASSWORD = 'test'
    PG_HOST = 'localhost'

    DATABASE_URI = 'postgres://{0}:{1}@{2}:5432/{3}'.format(
        PG_USER, PG_PASSWORD, PG_HOST, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}:5432/{3}'.format(
        PG_USER, PG_PASSWORD, PG_HOST, DB_NAME)

elif DB_TYPE == 'sqlite':
    DATABASE_URI = 'sqlite:///{0}.db'.format(DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}.db'.format(DB_NAME)

else:
    raise ValueError('DB_TYPE must be postgres or sqlite')


# False for performance reasons
SQLALCHEMY_TRACK_MODIFICATIONS = False

# path for admin file uploads
import os
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'
