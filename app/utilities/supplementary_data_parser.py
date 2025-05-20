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
    ITEM_IDENTIFIER_ERROR = (
        "Item identifier must be a non-empty string or non-negative integer"
    )

    @validates("identifier")
    def validate_identifier(  # pylint: disable=no-self-use
        self, identifier: fields.Field
    ) -> None:
        if not (isinstance(identifier, str) and identifier.strip()) and not (
            isinstance(identifier, int) and identifier >= 0
        ):
            raise ValidationError(self.ITEM_IDENTIFIER_ERROR)


class ItemsData(Schema, StripWhitespaceMixin):
    pass


class SupplementaryData(Schema, StripWhitespaceMixin):
    SDS_IDENTIFIER_ERROR = "Supplementary data did not return the specified Identifier"

    identifier = VALIDATORS["string"](validate=validate.Length(min=1))
    items = fields.Nested(ItemsData, required=False, unknown=INCLUDE)

    @validates_schema()
    def validate_identifier(  # pylint: disable=unused-argument
        self, data: Mapping, **kwargs: Any
    ) -> None:
        if data and data["identifier"] != self.context["identifier"]:
            raise ValidationError(self.SDS_IDENTIFIER_ERROR)


class SupplementaryDataMetadataSchema(Schema, StripWhitespaceMixin):
    DATASET_ID_ERROR = "Supplementary data did not return the specified Dataset ID"
    SURVEY_ID_ERROR = "Supplementary data did not return the specified Survey ID"
    MISMATCH_SDS_VERSION = "The Supplementary Dataset Schema Version does not match the version set in the Questionnaire Schema"
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
                raise ValidationError(self.DATASET_ID_ERROR)

            if payload["survey_id"] != self.context["survey_id"]:
                raise ValidationError(self.SURVEY_ID_ERROR)

            if self.context["sds_schema_version"] and (
                payload["data"]["schema_version"] != self.context["sds_schema_version"]
            ):
                raise ValidationError(self.MISMATCH_SDS_VERSION)


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
