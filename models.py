"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column (db.Integer,
                    primary_key = True, 
                    autoincrement = True)
    first_name = db.Column (db.String,
                            nullable = False)
    last_name = db.Column (db.String,
                            nullable = False)
    image_url = db.Column (db.String)

    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column (db.Integer,
                    primary_key = True, 
                    autoincrement = True)
    title = db.Column (db.String(50),
                       nullable = False)
    content = db.Column (db.Text, 
                         nullable = False)
    created_at = db.Column (db.DateTime, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    user = db.relationship('User', backref='posts'
                        #    cascade='all, delete-orphan', single_parent=True
                           )