from flask import Blueprint, Response, jsonify

from app.utilities.schema import get_schema_list, load_schema_from_name

schema_blueprint = Blueprint("schema", __name__)


@schema_blueprint.route("/schemas/<schema_name>", methods=["GET"])
def get_schema_json_from_name(schema_name: str) -> Response | tuple[str, int]:
    try:
        schema = load_schema_from_name(schema_name)
        return jsonify(schema.json)
    except FileNotFoundError:
        return "Schema Not Found", 404


@schema_blueprint.route("/schemas", methods=["GET"])
def list_schemas() -> Response:
    return jsonify(get_schema_list())
