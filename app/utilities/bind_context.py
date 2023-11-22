from structlog import contextvars

from app.data_models.metadata_proxy import MetadataProxy


def bind_contextvars_schema_from_metadata(metadata: MetadataProxy) -> None:
    """
    Metadata always contains exactly one way of identifying a schema, bind the reference to contextvars
    """
    if schema_name := metadata.schema_name:
        contextvars.bind_contextvars(schema_name=schema_name)

    if schema_url := metadata.schema_url:
        contextvars.bind_contextvars(schema_url=schema_url)

    if cir_instrument_id := metadata.cir_instrument_id:
        contextvars.bind_contextvars(cir_instrument_id=cir_instrument_id)
