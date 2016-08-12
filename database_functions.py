from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Image
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
                         hashed_password=hashed_password,
                         is_admin=False
                         ))
        session.commit()
        return True, uid
    else:
        return False, ''


def login(username, password):
    if username_is_taken(username):
        stored_user = session.query(User).filter(User.username == username).first()
        stored_password = stored_user.hashed_password
        stored_uid = stored_user.uid
        # Compared the newly encrypted password to the stored encrypted password
        if helper_functions.encrypt_password(stored_password, password) == stored_password:
            # User has correct password
            return True, stored_uid
    return False, ''


def new_image(title, owner, filename, iid=None):
    try:
        if iid is None:
            iid = helper_functions.generate_uid()
        session.add(Image(owner=owner,
                          title=title,
                          filename=filename,
                          likes=0,
                          iid=iid,
                          claimed=False
                          ))
        session.commit()
        return True, session.query(Image).filter(Image.iid == iid).first().iid
    except:
        return False, ''


def get_file_name_for_image(image_id):
    image = session.query(Image).filter(Image.iid == image_id).first()
    if image is not None:
        return True, image.filename
    else:
        return False, 'error.png'


def claim_image(title, owner, image_id):
    image = session.query(Image).filter(Image.iid == image_id).first()
    if image is not None:
        if image.owner == "unclaimed":
            image.owner = owner
            image.title = title
            image.claimed = True
            session.commit()
            return True
    return False

def like_image(image_id):
    image = session.query(Image).filter(Image.iid == image_id).first()
    if image is not None:
        image.likes += 1
        session.commit()
    return


def number_of_images():
    count = 0
    for image in session.query(Image).filter(Image.claimed == True).all():
        print(image.claimed)
        count += 1
    return count


def homepage_images():
    response = dict()
    """
    response = {
        images: [
            ["image_id", "image_title", "image_like_count"],
            ["image_id", "image_title", "image_like_count"]
        ]
    }
    """
    for image in session.query(Image).filter(Image.claimed == True).all():
        response.append
