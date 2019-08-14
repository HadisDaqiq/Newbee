"""Models and database functions for event Newbee database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User
"""user model"""
    
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True
                        )
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)\
    fav_sport = db.Column(db.String(50), nullable=True)

    photo = db.Column(db.String(100), nullable=True)



    def __repr__(self):
        """ show info aobut human"""
        return "<user id={} fname={} lname={} email={}> Username={} password={} fav_sport={} photo={}".format(
            self.user_id, self.fname self.lname, self.email, self.username, self.password self.fav_sport self.photo)




class Event(db.Model):
    """event table"""

    __tablename__ = "events"

    
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
                        nullable=False)



    def __repr__(self):
        """ show info aobut human"""
        return "<event id={} title={} description={} location={}> startData={} endDate={}".format(
            self.event_id, self.title, self.description, self.location, self.start_date, self.end_date)




class Sport(db.Model):
    """sport category table"""

    __tablename__ = "sport"

    fav_sport = db.Column(db.String(50), nullable=True)

    fav_sport = db.Column(db.Integer, db.ForeignKey('even.fav_sport '),
                        nullable=False)





class Register(db.Model):
    """events that you can register to"""

    __tablename__ = "register"


    fav_sport = db.Column(db.Integer, db.ForeignKey('even.fav_sport '),
                        nullable=False)

    fav_sport = db.Column(db.Integer, db.ForeignKey('even.fav_sport '),
                        nullable=False)


