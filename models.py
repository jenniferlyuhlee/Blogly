"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
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