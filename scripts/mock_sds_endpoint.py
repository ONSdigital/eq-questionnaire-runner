from flask import Flask, request, Response

app = Flask(__name__)

SUPPLEMENTARY_DATA_TILES_AND_SLATE_PAYLOAD = {
    "dataset_id": "001",
    "survey_id": "123",
    "data": {
        "schema_version": "v1",
        "identifier": "12346789012A",
        "items": {
            "local_units": [
                {
                    "identifier": "0001",
                    "lu_name": "TEST NAME. 1",
                    "lu_address": [
                        "FIRST ADDRESS 1",
                        "FIRST ADDRESS 2",
                        "TOWN",
                        "COUNTY",
                        "POST CODE",
                    ],
                },
                {
                    "identifier": "0002",
                    "lu_name": "TEST NAME 2",
                    "lu_address": [
                        "SECOND ADDRESS 1",
                        "SECOND ADDRESS 1",
                        "TOWN",
                        "COUNTY",
                        "POSTCODE",
                    ],
                },
            ]
        },
    },
}

SUPPLEMENTARY_DATA_PRODCOM_PAYLOAD = {
    "dataset_id": "002",
    "survey_id": "123",
    "data": {
        "schema_version": "v1",
        "identifier": "12346789012A",
        "note": {
            "title": "Volume of total production",
            "description": "Figures should cover the total quantity of the goods produced during the period of the return",
        },
        "items": {
            "products": [
                {
                    "identifier": "89929001",
                    "name": "Articles and equipment for sports or outdoor games",
                    "cn_codes": "2504 + 250610 + 2512 + 2519 + 2524",
                    "guidance_include": {
                        "title": "Include",
                        "list": [
                            "for children's playgrounds",
                            "swimming pools and paddling pools",
                        ],
                    },
                    "guidance_exclude": {
                        "title": "Exclude",
                        "list": [
                            "sports holdalls, gloves, clothing of textile materials, footwear, protective eyewear, rackets, balls, skates",
                            "for skiing, water sports, golf, fishing', for skiing, water sports, golf, fishing, table tennis, PE, gymnastics, athletics",
                        ],
                    },
                    "value_sales": {
                        "answer_code": "89929001",
                        "label": "Value of sales",
                    },
                    "volume_sales": {
                        "answer_code": "89929002",
                        "label": "Volume of sales",
                        "unit_label": "Tonnes",
                    },
                    "total_volume": {
                        "answer_code": "89929005",
                        "label": "Total volume produced",
                        "unit_label": "Tonnes",
                    },
                },
                {
                    "identifier": "201630601",
                    "name": "Other Minerals",
                    "cn_codes": "5908 + 5910 + 591110 + 591120 + 591140",
                    "guidance_include": {
                        "title": "Include",
                        "list": [
                            "natural graphite",
                            "quartz for industrial use",
                            "diatomite; magnesia; feldspar",
                            "magnesite; natural magnesium carbonate",
                            "talc including steatite and chlorite",
                            "unexpanded vermiculite and perlite",
                        ],
                    },
                    "guidance_exclude": {
                        "title": "Exclude",
                        "list": ["natural quartz sands"],
                    },
                    "value_sales": {
                        "answer_code": "201630601",
                        "label": "Value of sales",
                    },
                    "volume_sales": {
                        "answer_code": "201630602",
                        "label": "Volume of sales",
                        "unit_label": "Kilogram",
                    },
                    "total_volume": {
                        "answer_code": "201630605",
                        "label": "Total volume produced",
                        "unit_label": "Kilogram",
                    },
                },
            ]
        },
    },
}


@app.route("/v1/unit_data")
def get_sds_data():
    dataset_id = request.args.get("dataset_id")

    if dataset_id == "002":
        return SUPPLEMENTARY_DATA_PRODCOM_PAYLOAD
    elif dataset_id == "001":
        return SUPPLEMENTARY_DATA_TILES_AND_SLATE_PAYLOAD
    else:
        return Response(status=404)


if __name__ == "__main__":
    app.run(host="localhost", port=5003)
