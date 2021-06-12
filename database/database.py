from sqlalchemy import desc

from database.DatabaseResult import DatabaseResult
from database.connect_to_database import loadSession
from database.models import HrPartners, Interviews, Applications, Users


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


def get_application(application_id: int):
    session = loadSession()
    application = session.query(Applications).get(application_id)
    return application


def get_user(user_id: int):
    session = loadSession()
    user = session.query(Users).get(user_id)
    return user


def get_user_from_interview_uuid(interview_uuid: str) -> (DatabaseResult, str):
    session = loadSession()
    interviews = session.query(Interviews).filter(Interviews.id == interview_uuid)
    if interviews.count() == 0:
        return DatabaseResult.DONT_EXIST, f"Interview with id: {interview_uuid} doesn't exist"

    interview = interviews[0]
    application = get_application(interview.application)
    user = get_user(application.jobSeeker)
    return DatabaseResult.SUCCESS, user
