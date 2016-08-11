from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import config

Base = declarative_base()


# The table for user accounts.
class User(Base):
    __tablename__ = 'Users'
    pk = Column(Integer, primary_key=True)
    uid = Column(String())
    username = Column(String())
    hashed_password = Column(String())
    is_admin = Column(Boolean)


class Image(Base):
    __tablename__ = 'Images'
    pk = Column(Integer, primary_key=True)
    iid = Column(String())
    title = Column(String())
    likes = Column(Integer)
    owner = Column(String())  # The uid of the image uploader
    filename = Column(String())

# Create an engine that stores data in the local directory's
# database.db file.
engine = create_engine(config.path_to_db())

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)