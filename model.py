"""Models and database functions for event Newbee database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """user model"""
    
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True
                        )
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bio= db.Column(db.String(50), nullable=True)

    photo_url = db.Column(db.String(100), nullable=True)



    def __repr__(self):
        """ show info aobut human"""
        return "<user id={} fname={} lname={} email={}>Username={} password={} bio={} photo={}".format(
            self.user_id, self.fname, self.lname, self.email, 
            self.username, self.password, self.bio, self.photo_url
            )



class Event(db.Model):
    """event table"""

    __tablename__ = "event"

    
    event_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True
                        )
    title = db.Column(db.String(100), nullable=False)
    description =db.Column(db.String(300), nullable=True)
    location = db.Column(db.String(300), nullable=True)
    start_date = db.Column(db.String(30), nullable=False)
    end_date = db.Column(db.String(30), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.sport_id'),
                        nullable=False) #sport is massured in what event they attend to.



    def __repr__(self):
        """ show info aobut human"""
        return ("<event id={} title={} description={}"
                " location={}> startData={} endDate={}").format(
            self.event_id, self.title, self.description, 
            self.location, self.start_date, self.end_date)




class Sport(db.Model):
    """sport category table"""

    __tablename__ = "sport"

    sport_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)

    sport_name = db.Column(db.String(50), nullable=True)

    





class Register(db.Model):
    """events that you can register to"""

    __tablename__ = "register"


    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_idr '),
                        nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'),
                        nullable=False)

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





