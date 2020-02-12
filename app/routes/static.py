import json

from flask import Blueprint, jsonify
from structlog import get_logger

from app.helpers.language_helper import handle_language
from app.helpers.template_helper import render_template

logger = get_logger()

static_blueprint = Blueprint(name="static", import_name=__name__)


@static_blueprint.before_request
def before_static_request():
    handle_language()


@static_blueprint.route("/privacy", methods=["GET"])
def privacy():
    return render_template("static/privacy")


@static_blueprint.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("static/accessibility")


# This is not the recommended way of serving static files and
# is made available for testing purposes only due to runners content
# security policy. It should be removed once the json is available within CDN
@static_blueprint.route("/json/countries", methods=["GET"])
def countries():
    with open("templates/static/json/country-of-birth.json") as countries_file:
        country_data = json.load(countries_file)
        return jsonify(country_data)
