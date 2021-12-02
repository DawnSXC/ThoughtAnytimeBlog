from app import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.now)
    browsing_times = db.Column(db.Integer, default=0)
    like_times = db.Column(db.Integer, default=0)
    dislike_times = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    post_img = db.Column(db.String(1000))
    post_comments = db.relationship('Comment', backref='post')
    collected = db.relationship('Collect', backref='post')


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_time = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment


class Collect(db.Model):
    __tablename__ = "collect"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(30), nullable=False)
    post = db.relationship('Post', backref='category')
