
"""Events adding."""
import os
from dateutil.parser import parse
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import or_
from model import User, Event, Sport, Register, connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get("secret_key")

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
searchedEvents = None

@app.route('/')
def index():
    """Homepage"""
    if  session.get('user') == None:
        return redirect('/showlog')

    if searchedEvents == None:
        events = Event.query.all()
        #redirect = "login.html"
    else:
        events = searchedEvents
        #redirect = "homepage.html"

    for event in events:
        if event.date !=None and event.time !=None:
            format = '%a %I:%M %p %b %d, %y'
        
            event.date = event.date.strftime(format)
            event.time = event.time.strftime(format)
            
            print(">>>>>>>>>>>>>>>>>>SfSFSFSDfs",event.date, event.time)

       

    sports = Sport.query.all()
    image_urls ={}

    for sport in sports:
        image_urls[sport.sport_id] = sport.img_url

 
    # queries all the events for the currect user. 
    if session.get('user') == None:
        joined_events = []
    else:
        joined_events_query = db.session.query(Register.event_id).filter(Register.user_id == session['user']).all()
        joined_events= [value for (value,) in joined_events_query]
        print("@@@@@@@@@@@@@@@@@@@",joined_events)
    # print('>>>>>>>>', events_test)

    return render_template("homepage.html", events=events, sports = sports, joined_events = joined_events, image_urls = image_urls)




@app.route('/showlog')
def show_login_form():
    """show login form"""

    return render_template("login.html")



@app.route('/register')
def register_form():
    """Show Registration form """

    return render_template("registration_form.html")




@app.route('/signup', methods =["POST"])
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
    if User.query.filter(User.email == email).first() and User.query.filter(User.password == password).first():
        return redirect('/') 

    else:
        user= User(fname = fname, lname = lname, email = email,
           password = password, bio = bio, photo = photo)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

        


@app.route('/login', methods=['POST'])
def login_form():
    """authenticate user information"""
    email = request.form.get("email")
    password = request.form.get("password")

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


@app.route('/login_alert')
def login_alert():
    """returns alert cant access if not loged in"""
    alert("Sign up / Login To Join")
    return redirect('/')


@app.route('/logout')
def logout():
    """logs out the current user"""
    session.clear()
    return redirect("/showlog")


@app.route('/search')
def search():
    """logs out the current user"""
    searchKeyword = request.args.get("searchKeyword")
    search = "%{}%".format(searchKeyword)
    #events = db.session.query(Event).filter(or_(Event.title.ilike(search), Event.description.ilike(search))).all()
    events = []



    sports = db.session.query(Sport).filter(Sport.sport_name.ilike(search)).all()
    print("#################################", sports)
    for sport in sports:
        eventList = db.session.query(Event).filter(Event.sport_id == sport.sport_id).all()
        for event in eventList:
            events.append(event)
            # global searchedEvents
            # searchedEvents = events


    for event in events:
        if event.date !=None and event.time !=None:
            format = '%a %I:%M %p %b %d, %y'
        
            event.date = event.date.strftime(format)
            event.time = event.time.strftime(format)
            


    image_urls ={}

    for sport in sports:
        image_urls[sport.sport_id] = sport.img_url

    print('>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<s',events)
    return render_template('search.html', events=events, image_urls=image_urls, sports=sports)




@app.route('/event')
def event_process():
    """ add event form ("save-event-popup") and add it to the db"""

    title = request.args.get("title")
    description = request.args.get("des")
    location = request.args.get("location")
    start_date_time = request.args.get("start_date_time")
    end_date_time = request.args.get("end_date_time")
    print("@@@@@@@@@@@@@@@@@@@@@@@",start_date_time, end_date_time)
    user_id = session['user']
    sport_id = request.args.get("sport")

    print("\n\n\SPORT: \n\n\n",sport_id)

    event = Event(title = title, description = description,
        location = location,date = start_date_time, time = end_date_time,
        user_id=user_id, sport_id=sport_id)

    print("\n\n\nevent: \n\n\n",event)
    db.session.add(event)
    db.session.commit()

    return redirect('/')


@app.route('/delete_event')
def delete_process():
    """deleting events from homepage"""
    # if the userid is the same as the events.user_id then show delete
    currentEventId = request.args.get("currentEventId")
    event_record = db.session.query(Event).filter(Event.event_id == currentEventId).first()

    if event_record.user_id == session['user']:
        # delete event that has the currentEventId
        delete_event = db.session.query(Event).filter(Event.event_id == currentEventId).first()
        print(delete_event)
        db.session.delete(delete_event)
        db.session.commit()
        flash("event deleted")

    return redirect('/')



@app.route('/event_detail')
def event_detail():
    """redirect event details and number of attendees of each event"""
    # getting event id from homepage 
    event_id = request.args.get('eventId')
    # counting the total number of registeration for an event.
    registrant_count = db.session.query(Register).filter(Register.event_id ==event_id).count()
    event = db.session.query(Event).filter(Event.event_id == event_id).first()
    format = '%a %I:%M %p %b %d, %y'
    event.date = event.date.strftime(format)
    event.time = event.time.strftime(format)
    location = event.location

    return render_template("event.html", event= event, registrant_count=registrant_count)




@app.route('/join')
def join():
    """allows user to join or leave event """
    # getting event id from homepage
    event_id = request.args.get('eventId')
    user_id = session['user']
    register = Register(user_id = user_id, event_id = event_id)
    db.session.add(register)
    db.session.commit()

    return redirect('/')



@app.route('/unjoin')
def unjoin():
    """allows the user to unjoin an event"""
    event_id = request.args.get('eventId')
    print("-=-=-=-=-",event_id)
    register = db.session.query(Register).filter(Register.event_id == event_id).first()
    db.session.delete(register)
    db.session.commit()
    
    return redirect('/')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at 
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
 
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
