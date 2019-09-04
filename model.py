"""Models and database functions for event Newbee database."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """user model"""
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True
                        )
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(50), nullable=True)
    photo =  db.Column(db.String(2000), nullable=True)


    def __repr__(self):
        """ show info aobut human"""
        return "<user id={} fname={} lname={} email={}>password={} bio={} photo{}".format(
            self.user_id, self.fname, self.lname, self.email,
             self.password, self.bio, self.photo
            )


class Event(db.Model):
    """event table"""

    __tablename__ = "events"

    
    event_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True
                        )
    title = db.Column(db.String(100), nullable=False)
    description =db.Column(db.String(300), nullable=True)
    location = db.Column(db.String(300), nullable=True)
    expert_level = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime(), nullable=True)
    time = db.Column(db.DateTime(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.sport_id'),
                        nullable=False) #sport is massured in what event they attend to.

    def __repr__(self):
        """ show info about event"""
        return ("<event id={} title={} description={}"
                " location={}> date={} time={} ").format(
            self.event_id, self.title, self.description, 
            self.location, self.date, self.time)


class Sport(db.Model):
    """sport category table"""

    __tablename__ = "sports"

    sport_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)

    sport_name = db.Column(db.String(50), nullable=True)
    img_url =  db.Column(db.String(2000), nullable=True)

    def __repr__(self):
        """ show info aobut human"""
        return "<sport_id={} sport_name={} img_url{}".format(
            self.sport_id, self.sport_name, self.img_url
            )

class Register(db.Model):
    """events that you can register to"""

    __tablename__ = "registers"

    register_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'),
                        nullable=False)

    def __repr__(self):
        """ show info aobut human"""
        return "<register_id={}".format(
            self.register_id
            )

#Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///Newbee'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()





