from typing import Mapping

from marshmallow import (
    EXCLUDE,
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)

from app.authentication.auth_payload_versions import PrepopSchemaVersion
from app.utilities.metadata_parser_v2 import VALIDATORS, StripWhitespaceMixin


class ItemsSchema(Schema):
    identifier = VALIDATORS["string"](validate=validate.Length(min=1))


class ItemsData(Schema, StripWhitespaceMixin):
    pass


class PrepopData(Schema, StripWhitespaceMixin):
    identifier = VALIDATORS["string"](validate=validate.Length(min=1))
    schema_version = VALIDATORS["string"](
        validate=validate.OneOf([PrepopSchemaVersion.V1.value])
    )
    items = fields.Nested(ItemsData, required=False, unknown=EXCLUDE)

    @validates_schema()
    def validate_unit_id(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        if (
            data
            and data.get("identifier")
            and data["identifier"] != self.context["ru_ref"]
        ):
            raise ValidationError("Prepop data did not return the specified Unit ID")


class PrepopMetadataSchema(Schema, StripWhitespaceMixin):
    dataset_id = VALIDATORS["string"](validate=validate.Length(min=1))
    survey_id = VALIDATORS["string"](validate=validate.Length(min=1))
    data = fields.Nested(
        PrepopData, required=True, unknown=EXCLUDE, validate=validate.Length(min=1)
    )

    @validates_schema()
    def validate_dataset_id(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        if (
            data
            and data.get("dataset_id")
            and data["dataset_id"] != self.context["dataset_id"]
        ):
            raise ValidationError("Prepop data did not return the specified Dataset ID")


def validate_prepop_data_v1(prepop_data: Mapping, dataset_id: str, ru_ref: str) -> dict:
    """Validate claims required for runner to function"""
    prepop_metadata_schema = PrepopMetadataSchema(unknown=INCLUDE)
    prepop_metadata_schema.context = {"dataset_id": dataset_id, "ru_ref": ru_ref}
    validated_prepop_data = prepop_metadata_schema.load(prepop_data)

    if prepop_items := prepop_data.get("data", {}).get("items"):
        for key, values in prepop_items.items():
            items = [ItemsSchema(unknown=INCLUDE).load(value) for value in values]
            validated_prepop_data["data"]["items"][key] = items

    return validated_prepop_data
