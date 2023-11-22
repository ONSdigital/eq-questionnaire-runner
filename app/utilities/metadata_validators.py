from marshmallow import fields, validate


class RegionCode(validate.Regexp):
    """A region code defined as per ISO 3166-2:GB
    Currently, this does not validate the subdivision, but only checks length
    """

    def __init__(self, *args, **kwargs):
        super().__init__("^GB-[A-Z]{3}$", *args, **kwargs)


class UUIDString(fields.UUID):
    """Currently, runner cannot handle UUID objects in metadata
    Since all metadata is serialized and deserialized to JSON.
    This custom field deserializes UUIDs to strings.
    """

    def _deserialize(self, *args, **kwargs):
        return str(super()._deserialize(*args, **kwargs))


class DateString(fields.DateTime):
    """Currently, runner cannot handle Date objects in metadata
    Since all metadata is serialized and deserialized to JSON.
    This custom field deserializes Dates to strings.
    """

    def _deserialize(self, *args, **kwargs):
        date = super()._deserialize(*args, **kwargs)

        if self.format == "iso8601":
            return date.isoformat()

        return date.strftime(self.format)
