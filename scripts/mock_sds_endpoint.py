import json

import yaml
from flask import Flask, Response, request
from sdc.crypto.jwe_helper import JWEHelper
from sdc.crypto.key_store import KeyStore

from app.keys import KEY_PURPOSE_SDS

app = Flask(__name__)
with open("dev-keys.yml", encoding="UTF-8") as keys_file:
    keys = KeyStore(yaml.safe_load(keys_file))


@app.route("/v1/unit_data")
def get_sds_data():
    dataset_id = request.args.get("dataset_id")

    guid_filename_map = {
        "c067f6de-6d64-42b1-8b02-431a3486c178": "supplementary_data",
        "693dc252-2e90-4412-bd9c-c4d953e36fcd": "supplementary_data_v2",
    }

    if filename := guid_filename_map.get(dataset_id):
        return encrypt_mock_data(load_mock_data(f"scripts/mock_data/{filename}.json"))

    return Response(status=404)


@app.route("/v1/dataset_metadata")
def get_sds_dataset_ids():
    survey_id = request.args.get("survey_id")
    period_id = request.args.get("period_id")

    return load_mock_sds_dataset_metadata(survey_id, period_id)


def load_mock_data(filename):
    with open(filename, encoding="utf-8") as mock_data_file:
        return json.load(mock_data_file)


def load_mock_sds_dataset_metadata(survey_id: str, period_id: str):
    del period_id  # not required for mock

    survey_id_filename_map = {
        "123": "supplementary_dataset_metadata_response",
    }

    if filename := survey_id_filename_map.get(survey_id):
        return load_mock_data(f"scripts/mock_data/{filename}.json")

    return Response(status=404)


def encrypt_mock_data(mock_data):
    key = keys.get_key(purpose=KEY_PURPOSE_SDS, key_type="private")
    mock_data["data"] = JWEHelper.encrypt_with_key(
        json.dumps(mock_data["data"]), key.kid, key.as_jwk()
    )
    return mock_data


if __name__ == "__main__":
    app.run(host="localhost", port=5003)
