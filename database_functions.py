from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User
import helper_functions
import config

# Connects to the database
engine = create_engine(config.path_to_db())
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def username_is_taken(username):
    if session.query(User).filter(User.username == username).first() is not None:
        return True
    else:
        return False


def create_user(username, password):
    # Here is where we check that the username isn't already taken
    if username_is_taken(username) is False:
        # Generating our uid.
        # The uid is what the user will use to identify themselves
        # the user will obtain their uid after logging in
        uid = helper_functions.generate_uid()
        hashed_password = helper_functions.encrypt_new_password(password)
        session.add(User(uid=uid,
                         username=username,
                         hashed_password=hashed_password
                         ))
        session.commit()
        return True, uid
    else:
        return False, ''