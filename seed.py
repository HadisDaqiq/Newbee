
from sqlalchemy import func
from model import User
from model import Register
from model import Sport
from model import Event


from model import connect_to_db, db

from datetime import datetime















if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_user()
    load_event()
    load_register()
    load_sport()