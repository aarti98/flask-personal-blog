import os

basedir = os.path.abspath(os.path.dirname(__file__))

# SECRET_KEY = '<^>YOUR_SECRET_KEY^>'
# SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'


SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-cannot-guess-this'

SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')