from email.policy import default
from app import db
from datetime import datetime
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(80), index=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return 'User {}'.format(self.name)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

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