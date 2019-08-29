
"""Events adding."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Event, Sport, Register, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""
    print(">>>>>>>>>>>>>>>>>>>>>>here<<<<<<<<<<<<<<<<<<<<<<<<<")
    if  session.get('user') == None:
        return redirect('/login')

    events = Event.query.all()
    sports = Sport.query.all()
    return render_template("homepage.html", events=events, sports=sports)


@app.route('/register')
def register_form():
    """Show Registration form"""

    return render_template("registration_form.html")

#user is already loged in. get users info and add it to the event list, 
#list of users who have registered to that event. 

@app.route('/join', methods =["POST"])
def register_process():
    """Process Registration form"""

    email = request.form.get("email")
    password = request.form.get("password")

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    bio   = request.form.get("bio")
    photo = request.form.get("photo")


    user = User()
    # if User.query.filter(User.email.in_(email)):
    if User.query.filter(User.email == email).first():
        return redirect('/') 

    else:
        user= User(fname = fname, lname = lname, email = email,
         password = password, bio = bio, photo_url = photo)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

        

@app.route('/showlog')
def show_login_form():
    """show login form"""

    return render_template("login.html")


@app.route('/login')
def login_form():
    email = request.args.get("email")
    password = request.args.get("password")

    # user = db.session.query(User.email).filter(User.email == email).first()

    userinfo = db.session.query(User).filter(User.email == email).first()

    if userinfo is None:
        flash("user not found")
        return redirect('/showlog')



    if userinfo.password == password and userinfo.email == email:

        print(">>>>>>>>>>>>>>>>>>>>>>",userinfo)
        # print("==>",record.user_id)
        session['user'] = userinfo.user_id
        flash("logged in as %s" % userinfo.user_id)
        return redirect('/')
    else:
        flash("wrong password or email")
        return redirect('/showlog')



@app.route('/event')
def event_process():
    """renders information from homepage, 
    add event form ("save-event-popup") and add it to the db"""
    print("look this time is real")

    title = request.args.get("title")
    description = request.args.get("des")
    location = request.args.get("location")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    user_id = 1
    sport_id = request.args.get("sport")

    photo = request.files['file']

    print("\n\n\SPORT: \n\n\n",sport_id)

    event = Event(title = title, description = description,
        location = location, start_date = start_date,
         end_date = end_date, user_id=user_id, sport_id=sport_id)

    print("\n\n\nevent: \n\n\n",event)

    db.session.add(event)
    db.session.commit()

    return redirect('/')


@app.route('/delete_event')
def delete_process():

    # if the userid is the same as the events.user_id then...

    currentEventId = request.args.get("currentEventId")
    print(">>>>>>>>>>>>>>>>>>>", currentEventId)

    event_record = db.session.query(Event).filter(Event.event_id == currentEventId).first()

    if event_record.user_id == session['user']:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>@@@@@@@@@@@@@")
        # delete event that has the currentEventId
        delete_event = db.session.query(Event).filter(Event.event_id == currentEventId).first()
        print(delete_event)
        db.session.delete(delete_event)
        db.session.commit()
        flash("event deleted")
       
    return redirect('/')

    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
