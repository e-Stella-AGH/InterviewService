from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
import json
from os.path import isfile

db_key = "DATABASE_URL"


def get_attribute(key: str):
    filename = "./config.json"
    if not isfile(filename):
        print("Problem with file")
        return None

    with open(filename) as json_file:
        data = json.load(json_file)
        if key in data:
            return data[key]
        else:
            print("No key in file")
            return None


uri = environ[db_key] if db_key in environ else get_attribute(db_key)

if uri is not None and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
if uri is not None:
    # For debug
    # engine = create_engine(uri, echo=True)
    engine = create_engine(uri, echo=False)
    Base = declarative_base(engine)
else:
    Base = None


def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
