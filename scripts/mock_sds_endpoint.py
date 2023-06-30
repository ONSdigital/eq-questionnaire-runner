import json

from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/v1/unit_data")
def get_sds_data():
    dataset_id = request.args.get("dataset_id")

    if dataset_id == "c067f6de-6d64-42b1-8b02-431a3486c178":
        return load_mock_data("scripts/mock_data/supplementary_data_no_repeat.json")
    if dataset_id == "34a80231-c49a-44d0-91a6-8fe1fb190e64":
        return load_mock_data("scripts/mock_data/supplementary_data_with_repeat.json")
    if dataset_id == "6b378962-f0c7-4e8c-947e-7d24ee1b6b88":
        return load_mock_data(
            "scripts/mock_data/supplementary_data_with_repeat_v2.json"
        )

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
    if survey_id == "123":
        return load_mock_data(
            "scripts/mock_data/supplementary_dataset_metadata_response.json"
        )

    return Response(status=404)


if __name__ == "__main__":
    app.run(host="localhost", port=5003)
