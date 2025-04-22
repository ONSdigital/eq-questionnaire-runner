from typing import Any, Mapping

from marshmallow import (
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)

from app.utilities.metadata_parser_v2 import VALIDATORS, StripWhitespaceMixin


class ItemsSchema(Schema):
    identifier = fields.Field(required=True)

    @validates("identifier")
    def validate_identifier(  # pylint: disable=no-self-use
        self, identifier: fields.Field
    ) -> None:
        if not (isinstance(identifier, str) and identifier.strip()) and not (
            isinstance(identifier, int) and identifier >= 0
        ):
            item_identifier_error_msg = "Item identifier must be a non-empty string or non-negative integer"
            raise ValidationError(
                item_identifier_error_msg
            )


class ItemsData(Schema, StripWhitespaceMixin):
    pass


class SupplementaryData(Schema, StripWhitespaceMixin):
    identifier = VALIDATORS["string"](validate=validate.Length(min=1))
    items = fields.Nested(ItemsData, required=False, unknown=INCLUDE)

    @validates_schema()
    def validate_identifier(  # pylint: disable=unused-argument
        self, data: Mapping, **kwargs: Any
    ) -> None:
        if data and data["identifier"] != self.context["identifier"]:
            identifier_error_msg = "Supplementary data did not return the specified Identifier"
            raise ValidationError(
            identifier_error_msg
            )


class SupplementaryDataMetadataSchema(Schema, StripWhitespaceMixin):
    dataset_id = VALIDATORS["uuid"]()
    survey_id = VALIDATORS["string"](validate=validate.Length(min=1))
    data = fields.Nested(
        SupplementaryData,
        required=True,
        unknown=INCLUDE,
        validate=validate.Length(min=1),
    )

    @validates_schema()
    def validate_payload(  # pylint: disable=unused-argument
        self, payload: Mapping, **kwargs: Any
    ) -> None:
        if payload:
            if payload["dataset_id"] != self.context["dataset_id"]:
                dataset_id_error_msg = "Supplementary data did not return the specified Dataset ID"
                raise ValidationError(
                dataset_id_error_msg
                )

            if payload["survey_id"] != self.context["survey_id"]:
                survey_id_error_msg = "Supplementary data did not return the specified Survey ID"
                raise ValidationError(
                    survey_id_error_msg
                )

            if self.context["sds_schema_version"] and (
                payload["data"]["schema_version"] != self.context["sds_schema_version"]
            ):
                mismatch_version_error_msg = "The Supplementary Dataset Schema Version does not match the version set in the Questionnaire Schema"
                raise ValidationError(
                    mismatch_version_error_msg
                )


def validate_supplementary_data_v1(
    supplementary_data: Mapping,
    dataset_id: str,
    identifier: str,
    survey_id: str,
    sds_schema_version: str | None = None,
) -> dict[str, str | dict | int | list]:
    """Validate claims required for supplementary data"""
    supplementary_data_metadata_schema = SupplementaryDataMetadataSchema(
        unknown=INCLUDE
    )
    supplementary_data_metadata_schema.context = {
        "dataset_id": dataset_id,
        "identifier": identifier,
        "survey_id": survey_id,
        "sds_schema_version": sds_schema_version,
    }
    validated_supplementary_data = supplementary_data_metadata_schema.load(
        supplementary_data
    )

    if supplementary_data_items := supplementary_data.get("data", {}).get("items"):
        for key, values in supplementary_data_items.items():
            items = [ItemsSchema(unknown=INCLUDE).load(value) for value in values]
            validated_supplementary_data["data"]["items"][key] = items

    # Type ignore: the load method in the Marshmallow parent schema class doesn't have type hints for return
    return validated_supplementary_data  # type: ignore
