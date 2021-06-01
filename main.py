from fastapi import Depends, FastAPI, HTTPException
from datetime import date
from typing import Dict
from database import get_organization_uuid_from_hrpartner, get_interview_uuid_from_application_id, DatabaseResult

app = FastAPI()


@app.get("/interview/{hr_partner_id}/{application_id}")
async def get_links(hr_partner_id: int, application_id: int, which: int = 0):
    organization_id = get_organization_uuid_from_hrpartner(hr_partner_id)
    if organization_id[0] == DatabaseResult.FAILURE:
        raise HTTPException(status_code=404, detail="This hrpartner doesn't exists")
    interview_id = get_interview_uuid_from_application_id(application_id, which)
    if interview_id[0] == DatabaseResult.FAILURE:
        raise HTTPException(status_code=404, detail="This application doesn't have got interviews")
    if interview_id[0] == DatabaseResult.DONT_EXIST:
        raise HTTPException(status_code=404, detail=f"This application doesn't have got {which + 1} interviews")
    job_seeker_link = f"/interview/{interview_id[1]}"
    admin_link = f"{job_seeker_link}/{organization_id[1]}"
    return {
        "admin": admin_link,
        "job_seeker": job_seeker_link
    }
