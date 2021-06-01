from sqlalchemy import desc


from DatabaseResult import DatabaseResult
from connect_to_database import loadSession
from models import HrPartners, Interviews


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
