from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(80), index=True)
    password_hash = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return 'User {}'.format(self.name)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    
    def __repr__(self):
        return 'Body <>'.format(self.body)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), index=True)
    description = db.Column(db.Text(), index=True)
    content = db.Column(db.Text(), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    comments = db.relationship('Comment', backref='commented_by', lazy='dynamic')

    def __repr__(self):
        return 'Title <>'.format(self.title)