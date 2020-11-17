from flask import Blueprint, jsonify

from app.utilities.schema import (
    DEFAULT_LANGUAGE_CODE,
    get_schema_path_map,
    load_schema_from_name,
)

schema_blueprint = Blueprint("schema", __name__)


@schema_blueprint.route("/schemas/<schema_name>", methods=["GET"])
def get_schema_json_from_name(schema_name):
    try:
        schema = load_schema_from_name(schema_name)
        return jsonify(schema.json)
    except FileNotFoundError:
        return "Schema Not Found", 404


@schema_blueprint.route("/schemas", methods=["GET"])
def list_schemas():
    default_schema_map = get_schema_path_map().get(DEFAULT_LANGUAGE_CODE)

    return jsonify(list(default_schema_map.keys()))
