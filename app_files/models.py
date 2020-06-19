from app_files import db
from datetime import datetime
from flask_login import UserMixin


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # user.id is lowercase because referencing the table name, which is user by default
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='post_src', lazy=True)

    def __repr__(self):
        return f'<Post: id={self.id}, author={self.author}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Todo: write encryption
    password = db.Column(db.String(60), nullable=False)

    # Relationship to post model
    # lazy means sqlalchemy will load all of the data in one go
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User: id={self.id}, name={self.username}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # The author of the comment
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # The post under which the comment was written
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)




