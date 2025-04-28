import functools
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, MutableMapping

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
    def strip_whitespace(  # pylint: disable=no-self-use, unused-argument
        self, items: MutableMapping, **kwargs: Any
    ) -> MutableMapping:
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
    def validate_receipting_keys(  # pylint: disable=no-self-use, unused-argument
        self, data: Mapping, **kwargs: Any
    ) -> None:
        if data and (receipting_keys := data.get("receipting_keys", {})):
            missing_receipting_keys = [
                receipting_key
                for receipting_key in receipting_keys
                if receipting_key not in data.get("data", {})
            ]

            if missing_receipting_keys:
                missing_keys_message = f"Receipting keys: {missing_receipting_keys} not set in Survey Metadata"
                raise ValidationError(missing_keys_message)


class RunnerMetadataSchema(Schema, StripWhitespaceMixin):
    """Metadata which is required for the operation of runner itself"""

    jti = VALIDATORS["uuid"]()
    tx_id = VALIDATORS["uuid"]()
    case_id = VALIDATORS["uuid"]()
    collection_exercise_sid = VALIDATORS["string"](validate=validate.Length(min=1))
    version = VALIDATORS["string"](
        required=True, validate=validate.OneOf([AuthPayloadVersion.V2.value])
    )
    schema_name = VALIDATORS["string"](required=False)
    schema_url = VALIDATORS["url"](required=False)
    cir_instrument_id = VALIDATORS["uuid"](required=False)
    response_id = VALIDATORS["string"](required=True)
    account_service_url = VALIDATORS["url"](required=True)

    language_code = VALIDATORS["string"](required=False)
    channel = VALIDATORS["string"](required=False, validate=validate.Length(min=1))
    response_expires_at = VALIDATORS["iso_8601_date_string"](
        required=True,
        validate=lambda x: parse_iso_8601_datetime(x) > datetime.now(tz=timezone.utc),
    )
    region_code = VALIDATORS["string"](required=False, validate=RegionCode())

    roles = fields.List(fields.String(), required=False)
    survey_metadata = fields.Nested(SurveyMetadata, required=False)

    @validates_schema
    def validate_schema_options(  # pylint: disable=no-self-use, unused-argument
        self, data: Mapping, **kwargs: Any
    ) -> None:
        if data:
            options = [
                option
                for option in ["schema_name", "schema_url", "cir_instrument_id"]
                if data.get(option)
            ]
            if len(options) == 0:
                missing_metadata_option = "Neither schema_name, schema_url or cir_instrument_id has been set in metadata"
                raise ValidationError(missing_metadata_option)
            if len(options) > 1:
                invalid_metadata_combination = (
                    "Only one of schema_name, schema_url or cir_instrument_id should be specified "
                    f"in metadata, but {', '.join(options)} were provided"
                )
                raise ValidationError(invalid_metadata_combination)


def validate_questionnaire_claims(
    claims: Mapping,
    questionnaire_specific_metadata: Iterable[Mapping],
    unknown: str = EXCLUDE,
) -> dict:
    """Validate any survey specific claims required for a questionnaire"""
    dynamic_fields: dict[str, fields.String | DateString] = {}

    for metadata_field in questionnaire_specific_metadata:
        field_arguments: dict[str, bool] = {}
        validators: list[validate.Validator] = []

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
    # Type ignore: the load method in the Marshmallow parent schema class doesn't have type hints for return
    return questionnaire_metadata_schema.load(claims)  # type: ignore


def validate_runner_claims_v2(claims: Mapping) -> dict:
    """Validate claims required for runner to function"""
    runner_metadata_schema = RunnerMetadataSchema(unknown=EXCLUDE)
    # Type ignore: the load method in the Marshmallow parent schema class doesn't have type hints for return
    return runner_metadata_schema.load(claims)  # type: ignore
