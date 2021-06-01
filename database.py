from enum import Enum
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
import json
from os.path import isfile

db_key = "DATABASE_URL"


def get_attribute(key: str):
    filename = "config.json"
    if not isfile(filename):
        return None

    with open(filename) as json_file:
        data = json.load(json_file)
        if key in data:
            return data[key]
        else:
            return None


uri = environ[db_key] if db_key in environ else get_attribute(db_key)

if uri is not None and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# For debug engine = create_engine(uri, echo=True)
engine = create_engine(uri, echo=False)
Base = declarative_base(engine)


def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class Interviews(Base):
    """"""
    __tablename__ = 'interviews'
    __table_args__ = {'autoload': True}


class HrPartners(Base):
    """"""
    __tablename__ = 'hrpartners'
    __table_args__ = {'autoload': True}


class DatabaseResult(Enum):
    FAILURE = 1
    DONT_EXIST = 2
    SUCCESS = 3


def get_organization_uuid_from_hrpartner(hr_partner: int) -> (DatabaseResult, str):
    session = loadSession()
    hrpartners = session.query(HrPartners).filter(HrPartners.id == hr_partner)
    hrpartners_count = hrpartners.count()
    if hrpartners_count == 0:
        return DatabaseResult.FAILURE, ""
    else:
        return DatabaseResult.SUCCESS, hrpartners[0].organization_id


def get_interview_uuid_from_application_id(application_id: int, which: int) -> (DatabaseResult, str):
    session = loadSession()
    interviews = session.query(Interviews).order_by(desc(Interviews.date_time)).filter(
        Interviews.application_id == application_id)
    interviews_count = interviews.count()
    if interviews_count == 0:
        return DatabaseResult.FAILURE, ""
    elif interviews_count <= which:
        return DatabaseResult.DONT_EXIST, ""
    else:
        return DatabaseResult.SUCCESS, interviews[which].id
