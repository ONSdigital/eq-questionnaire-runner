import functools
from datetime import datetime, timezone
from typing import Callable, Iterable, Mapping

from marshmallow import (
    EXCLUDE,
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    pre_load,
    validate,
    validates_schema,
)
from structlog import get_logger

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.questionnaire.rules.utils import parse_iso_8601_datetime
from app.utilities.metadata_validators import DateString, RegionCode, UUIDString

logger = get_logger()

VALIDATORS: Mapping[str, Callable] = {
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
    def strip_whitespace(
        self, items, **kwargs
    ):  # pylint: disable=no-self-use, unused-argument
        for key, value in items.items():
            if isinstance(value, str):
                items[key] = value.strip()
        return items


class Data(Schema, StripWhitespaceMixin):
    pass


class SurveyMetadata(Schema, StripWhitespaceMixin):
    data = fields.Nested(Data, unknown=INCLUDE, validate=validate.Length(min=1))
    receipting_keys = fields.List(fields.String)

    @validates_schema
    def validate_receipting_keys(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        if data and (receipting_keys := data.get("receipting_keys", {})):
            missing_receipting_keys = [
                receipting_key
                for receipting_key in receipting_keys
                if receipting_key not in data.get("data", {})
            ]

            if missing_receipting_keys:
                raise ValidationError(
                    f"Receipting keys: {missing_receipting_keys} not set in Survey Metadata"
                )


class RunnerMetadataSchema(Schema, StripWhitespaceMixin):
    """Metadata which is required for the operation of runner itself"""

    jti = VALIDATORS["uuid"]()  # type:ignore
    tx_id = VALIDATORS["uuid"]()  # type:ignore
    case_id = VALIDATORS["uuid"]()  # type:ignore
    collection_exercise_sid = VALIDATORS["string"](
        validate=validate.Length(min=1)
    )  # type:ignore
    version = VALIDATORS["string"](
        required=True, validate=validate.OneOf([AuthPayloadVersion.V2.value])
    )  # type:ignore
    schema_name = VALIDATORS["string"](required=False)  # type:ignore
    schema_url = VALIDATORS["url"](required=False)  # type:ignore
    response_id = VALIDATORS["string"](required=True)  # type:ignore
    account_service_url = VALIDATORS["url"](required=True)  # type:ignore

    language_code = VALIDATORS["string"](required=False)  # type:ignore
    channel = VALIDATORS["string"](
        required=False, validate=validate.Length(min=1)
    )  # type:ignore
    response_expires_at = VALIDATORS["iso_8601_date_string"](
        required=True,
        validate=lambda x: parse_iso_8601_datetime(x) > datetime.now(tz=timezone.utc),
    )  # type:ignore
    region_code = VALIDATORS["string"](
        required=False, validate=RegionCode()
    )  # type:ignore

    roles = fields.List(fields.String(), required=False)
    survey_metadata = fields.Nested(SurveyMetadata, required=False)

    @validates_schema
    def validate_schema_name_is_set(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        if data and not (data.get("schema_name") or data.get("schema_url")):
            raise ValidationError(
                "Neither schema_name or schema_url has been set in metadata"
            )


def validate_questionnaire_claims(
    claims: Mapping,
    questionnaire_specific_metadata: Iterable[Mapping],
    unknown=EXCLUDE,
) -> dict:
    """Validate any survey specific claims required for a questionnaire"""
    dynamic_fields = {}

    for metadata_field in questionnaire_specific_metadata:
        field_arguments = {}
        validators = []

        if metadata_field.get("optional"):
            field_arguments["required"] = False

        if any(
            length_limit in metadata_field
            for length_limit in ("min_length", "max_length", "length")
        ):
            validators.append(
                validate.Length(
                    min=metadata_field.get("min_length"),
                    max=metadata_field.get("max_length"),
                    equal=metadata_field.get("length"),
                )
            )

        dynamic_fields[metadata_field["name"]] = VALIDATORS[metadata_field["type"]](
            validate=validators, **field_arguments
        )

    questionnaire_metadata_schema = type(
        "QuestionnaireMetadataSchema", (Schema, StripWhitespaceMixin), dynamic_fields
    )(unknown=unknown)

    # The load method performs validation.
    return questionnaire_metadata_schema.load(claims)


def validate_runner_claims_v2(claims: Mapping) -> dict:
    """Validate claims required for runner to function"""
    runner_metadata_schema = RunnerMetadataSchema(unknown=EXCLUDE)
    return runner_metadata_schema.load(claims)
