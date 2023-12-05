import functools
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping

from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,
    pre_load,
    validate,
    validates_schema,
)
from structlog import get_logger

from app.questionnaire.rules.utils import parse_iso_8601_datetime
from app.utilities.metadata_validators import DateString, UUIDString
from app.utilities.schema import get_schema_name_from_params

logger = get_logger()

VALIDATORS = {
    "date": functools.partial(DateString, format="%Y-%m-%d", required=True),
    "uuid": functools.partial(UUIDString, required=True),
    "boolean": functools.partial(fields.Boolean, required=True),
    "string": functools.partial(fields.String, required=True),
    "url": functools.partial(fields.Url, required=True),
    "iso_8601_date_string": functools.partial(
        DateString, format="iso8601", required=True
    ),
}


class StripWhitespaceMixin:
    @pre_load()
    def strip_whitespace(  # pylint: disable=no-self-use, unused-argument
        self, items: MutableMapping, **kwargs: Any
    ) -> MutableMapping:
        for key, value in items.items():
            if isinstance(value, str):
                items[key] = value.strip()
        return items


class RunnerMetadataSchema(Schema, StripWhitespaceMixin):
    """Metadata which is required for the operation of runner itself"""

    jti = VALIDATORS["uuid"]()  # type:ignore
    ru_ref = VALIDATORS["string"](validate=validate.Length(min=1))  # type:ignore
    collection_exercise_sid = VALIDATORS["string"](
        validate=validate.Length(min=1)
    )  # type:ignore
    tx_id = VALIDATORS["uuid"]()  # type:ignore
    response_id = VALIDATORS["string"](required=False)  # type:ignore

    account_service_url = VALIDATORS["url"](required=True)  # type:ignore
    case_id = VALIDATORS["uuid"]()  # type:ignore
    account_service_log_out_url = VALIDATORS["url"](required=False)  # type:ignore
    roles = fields.List(fields.String(), required=False)
    schema_url = VALIDATORS["url"](required=False)  # type:ignore
    language_code = VALIDATORS["string"](required=False)  # type:ignore
    channel = VALIDATORS["string"](
        required=False, validate=validate.Length(min=1)
    )  # type:ignore
    case_type = VALIDATORS["string"](required=False)  # type:ignore
    response_expires_at = VALIDATORS["iso_8601_date_string"](
        required=True,
        validate=lambda x: parse_iso_8601_datetime(x) > datetime.now(tz=timezone.utc),
    )  # type:ignore

    schema_name = VALIDATORS["string"](required=False)  # type:ignore

    # The following two parameters are for business schemas
    form_type = VALIDATORS["string"](required=False)  # type:ignore
    eq_id = VALIDATORS["string"](required=False)  # type:ignore

    @validates_schema
    def validate_schema_name(  # pylint: disable=no-self-use, unused-argument
        self, data: Mapping, **kwargs: Any
    ) -> None:
        """Function to validate the business schema parameters"""
        if not data.get("schema_name"):
            business_schema_claims = (
                data.get("eq_id"),
                data.get("form_type"),
            )
            if not all(business_schema_claims):
                raise ValidationError(
                    "Either 'schema_name' or 'eq_id' and 'form_type' must be defined"
                )

    @post_load
    def update_schema_name(  # pylint: disable=no-self-use, unused-argument
        self, data: MutableMapping, **kwargs: Any
    ) -> MutableMapping:
        """Function to transform parameters into a business schema"""
        if data.get("schema_name"):
            logger.info(
                "Using schema_name claim to specify schema, overriding eq_id and form_type"
            )
        else:
            data["schema_name"] = get_schema_name_from_params(
                data.get("eq_id"), data.get("form_type")
            )
        return data

    @post_load
    def update_response_id(  # pylint: disable=no-self-use, unused-argument
        self, data: MutableMapping, **kwargs: Any
    ) -> MutableMapping:
        """
        If response_id is present : return as it is
        If response_id is not present : Build response_id from ru_ref,collection_exercise_sid,eq_id and form_type
                                        and updates metadata with response_id


        """
        if data.get("response_id"):
            logger.info(
                "'response_id' exists in claims, skipping 'response_id' generation"
            )
            return data
        eq_id = data.get("eq_id")
        form_type = data.get("form_type")
        if eq_id and form_type:
            ru_ref = data["ru_ref"]
            collection_exercise_sid = data["collection_exercise_sid"]
            response_id = f"{ru_ref}{collection_exercise_sid}{eq_id}{form_type}"
            data["response_id"] = response_id
            return data

        raise ValidationError(
            "Both 'eq_id' and 'form_type' must be defined when 'response_id' is not defined"
        )


def validate_runner_claims(claims: Mapping) -> dict:
    """Validate claims required for runner to function"""
    runner_metadata_schema = RunnerMetadataSchema(unknown=EXCLUDE)
    # Type ignore: the load method in the Marshmallow parent schema class doesn't have type hints for return
    return runner_metadata_schema.load(claims)  # type: ignore
