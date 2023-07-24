# pylint: disable=redefined-outer-name
import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.authentication.auth_payload_versions import AuthPayloadVersion


def get_metadata(version):
    return (
        fake_metadata_runner_v2()
        if version is AuthPayloadVersion.V2
        else fake_metadata_runner()
    )


def get_metadata_full(version):
    return (
        fake_metadata_full_v2_business()
        if version is AuthPayloadVersion.V2
        else fake_metadata_full()
    )


def get_metadata_social():
    return fake_metadata_full_v2_social()


def fake_metadata_runner():
    """Generate the set of claims required for runner to function"""
    return {
        "tx_id": str(uuid.uuid4()),
        "jti": str(uuid.uuid4()),
        "schema_name": "2_a",
        "ru_ref": "2016-04-04",
        "collection_exercise_sid": "test-sid",
        "response_id": str(uuid.uuid4()),
        "account_service_url": "https://ras.ons.gov.uk",
        "case_id": str(uuid.uuid4()),
        "response_expires_at": get_response_expires_at(),
    }


@pytest.fixture()
def fake_business_metadata_runner():
    """Generate a set of claims required for runner using business parameters instead of schema_name"""
    metadata = get_metadata(version=None)
    del metadata["schema_name"]

    metadata["eq_id"] = "mbs"
    metadata["form_type"] = "0253"
    metadata["response_expires_at"] = get_response_expires_at()

    return metadata


def fake_metadata_full():
    """Generate a fake set of claims
    These claims should represent all claims known to runner, including common questionnaire
    level claims.
    """
    fake_questionnaire_claims = {
        "user_id": "1",
        "period_id": "3",
        "period_str": "2016-01-01",
        "ref_p_start_date": "2016-02-02",
        "ref_p_end_date": "2016-03-03",
        "ru_name": "Apple",
        "return_by": "2016-07-07",
        "case_ref": "1000000000000001",
        "case_id": str(uuid.uuid4()),
        "response_expires_at": get_response_expires_at(),
    }

    return dict(fake_metadata_runner(), **fake_questionnaire_claims)


def fake_metadata_runner_v2():
    """Generate the set of claims required for runner to function"""
    return {
        "tx_id": str(uuid.uuid4()),
        "jti": str(uuid.uuid4()),
        "schema_name": "2_a",
        "collection_exercise_sid": "test-sid",
        "response_id": str(uuid.uuid4()),
        "account_service_url": "https://ras.ons.gov.uk",
        "case_id": str(uuid.uuid4()),
        "version": AuthPayloadVersion.V2.value,
        "survey_metadata": {"data": {"key": "value"}},
        "response_expires_at": get_response_expires_at(),
    }


def fake_metadata_full_v2_business():
    """Generate a fake set of claims
    These claims should represent all claims known to runner, including common questionnaire
    level claims.
    """
    fake_survey_metadata_claims = {
        "user_id": "1",
        "period_id": "3",
        "period_str": "2016-01-01",
        "ref_p_start_date": "2016-02-02",
        "ref_p_end_date": "2016-03-03",
        "ru_name": "Apple",
        "return_by": "2016-07-07",
        "case_ref": "1000000000000001",
        "ru_ref": "123456789",
        "form_type": "I",
        "response_expires_at": get_response_expires_at(),
    }

    metadata = fake_metadata_runner_v2()

    metadata["survey_metadata"]["data"] = fake_survey_metadata_claims

    return metadata


def fake_metadata_full_v2_social():
    """Generate a fake set of claims
    These claims should represent all claims known to runner, including common questionnaire
    level claims.
    """
    fake_survey_metadata_claims = {
        "case_ref": "1000000000000001",
        "qid": "2000000000000002",
    }

    metadata = fake_metadata_runner_v2()

    metadata["survey_metadata"]["data"] = fake_survey_metadata_claims
    metadata["survey_metadata"]["receipting_keys"] = ["qid"]

    return metadata


@pytest.fixture
def fake_questionnaire_metadata_requirements_full():
    return [
        {"name": "user_id", "type": "string"},
        {"name": "period_id", "type": "string"},
        {"name": "period_str", "type": "string"},
        {"name": "ref_p_start_date", "type": "string"},
        {"name": "ref_p_end_date", "type": "string"},
        {"name": "account_service_url", "type": "url", "optional": True},
    ]


def get_response_expires_at() -> str:
    return (datetime.now(tz=timezone.utc) + timedelta(days=1)).isoformat()
