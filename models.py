import configparser
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

config = configparser.ConfigParser()
config.read("config.ini")

Base = declarative_base()


# the class needed to define the user object
class User(Base):
    __tablename__ = config['Database']['table']
    user_id = Column(Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = Column(String(100), unique=True)
    password = Column(String(100))

    def __repr__(self):
        return "<User(username='%s', password='%s')>" % (
                                 self.username, self.password)


