from DatabaseResult import DatabaseResult


def override_get_organization_uuid_from_hrpartner(hr_partner: int) -> (DatabaseResult, str):
    hrpartners_count = 1 if hr_partner == 5 else 0
    if hrpartners_count == 0:
        return DatabaseResult.FAILURE, ""
    else:
        return DatabaseResult.SUCCESS, "9ff2faff-dc3f-40b0-8c02-53a67750281e"


def override_get_interview_uuid_from_application_id(application_id: int, which: int) -> (DatabaseResult, str):
    interviews_count = 2 if application_id == 1 else 0
    if interviews_count == 0:
        return DatabaseResult.FAILURE, ""
    elif interviews_count <= which:
        return DatabaseResult.DONT_EXIST, ""
    else:
        return DatabaseResult.SUCCESS, "e1177e54-d903-4e91-a299-ddc56606785b" if which == 0 else "cbb6b884-888a-4ec4-9446-0a25ba2f2e9e"
