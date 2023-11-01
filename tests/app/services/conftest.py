import pytest


@pytest.fixture
def decrypted_mock_supplementary_data_payload():
    return {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
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


@pytest.fixture
def encrypted_mock_supplementary_data_payload():
    return {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        # pylint: disable-next=line-too-long
        "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk2In0.HXHbiTFa2XCuaKfSX4HfONLAVfZxEZo6_072A-ilMwhQKVhmQzqhDOX9dRID1yeoJnYxcdVGRDPwD5QvVHY2qsIOGkO3Brh59GHvSVASSCR21od7DBvlv0LoCDGAVcPt5bwwMbmziGQNkyfNnZG1EwAFk09lWfXwapJDsKbu1uhbW-F8HOOFZT7vR3paUmeTS0ekITwod-eZTD-B7KwUnDhJSm12cl9ob8MHirCaTE3jB64iQe_GvgdSUs1n5HZnX1f7rDQEpWm0OeuxPbEDrFmU-9wBV6LAjszypxPhQ0pv76TMu-VhjNBgf5Xm0cMO8ycmubdBdyWZiVUcmG0or9Mw0QvDYA9th27RChZPs5Le0w9oTnp5p5qzQexpPdzcS9Niqwabwx-NyUvTYkkFWc9poGNtrane4Ei4AFlV1-nQ4A8wMSIuOOSteYVombw-FEo9FhIhnuU8qyHoy0EaW5D1PMcdsphSb2ybTsiEJfdwwpxWDiuMDUpW6c2It_uSEpLCFHj51pQ8_Ez44gDyRE41NpSVvOB6h-nOggICQKggBDimtAuOyunZ5jhQWlKAeX4vAwM4iUEJ82c9lLTb8EDmQDOj6os9PCmyrZku5FHRXXDDvyuQAEqB-ARRnWT47LZOmaeTn4RI92qcejOqTNSG80mCUMY1PPu1fqxOiG8.5ukQQc5IT8fHgMRJ.jDXFWkIV9PIIrAC6EnVu5joGNdlmM52xgEqXCocUvZflvT8xMNocGGDUD1S0_FbQlpSP8FJcby4-B88yzxLgwil7mBqGtE7kWjALPGgnV9DsjEs-OblFFUIY9dVaKMTwaXhSxpjEt4j9NUOo-uyKOQIg-ZT745_zbkFZhlScuHz0u1YYaZGN04Md-eDI38erkTrS3pe2aovjbrwc9s_FMbrHEKlnuAUwxGPUxLTJXpTavHdmhhWriaI6a9ymng6mcefKqpNfWXc-3MIY2k10JCoo2KlVyYRN0up6T4OW56mAoXf7dUNSC8PtcZ5J3rpJ4XUnLZNVSL6Kz9BAmXY5SpZlU9zIBxHsirG9fS8gV6bI_MeMwbMawMCylcArlINVGVwDnUIvNXIJplVgm1OTHL0TiZzEFvnqkro3mzvVL-ElFeYO0uegqN8cDGkcv_lpAHH33j-IPdG-8CYerTCSVrT9.vWWMrdJFFLTVBSiv3KhbiQ",
    }


@pytest.fixture
def mock_supplementary_data_payload_invalid_kid_in_data():
    return {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        # pylint: disable-next=line-too-long
        "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk3In0=.lssJXsMUE3dhWtQRUt7DTaZJvx4DpNdLW98cu8g4NijYX9TFpJiOFyzPxUlpFZb-fMa4zW9q6qZofQeQTbl_Ae3QAwGhuWF7v9NMdWM1aH377byyJJyJpdqlU4t-P03evRWZqAG2HtsNE2Zn1ORXn80Dc9IRkzutgrziLI8OBIZeO6-XEgbVCapsQApWkyux7QRdFH95wfda75nVvGqTbBOYvQiMTKd8KzpH2Vl200IOqEpmrcjUCE-yqdTupzcr88hwNI2ZYdv-pTNowJw1FPODZ7V_sE4Ac-JYv3yBTDcXdz3I5-rX8i2HXqz-g3VhveZiAl9q0AgklPkaO_oNWJzjrCb7DZGL4DjiGYuOcw8OSdOpKLXwkExMlado-wigxy1IWoCzFu2E5tWpmLc0WWcjKuBgD7-4tcn059F7GcwhX2uMRESCmc39pblvseM2UnmmQnwr8GvD7gqWdFwtBsECyXQ5UXAxWLJor_MtU8lAFZxiorRcrXZJwAivroPO9iEB-1Mvt2zZFWI_vMgpJCAIpETscotDKMVCG0UMfkKckJqLnmQpvF4oYTr77w1COBX5bi-AV8UrLJ7sVVktSXOBc_KCGRpoImA5cE67hW7mFUdJi1EHA39qt0tTqZD7izpu8sSLxsiuCkfsqrd4uAedcDdQm4QGxXOPD4pxois.wfWsetB3M0x9qfw5.43Wns86lGlbHj63b0ZxE2bxBQVus6FIqelb9LfSbvopLn5oR8FM4vDEnDp_rIyvjmV9YAZJ6HAHaYaWoNyIO0EorgamrB4R3-LqInANoe9c8xLZ9wl_QpE9aWnxsmFGZUWLO3q2fVTPnwBtA_LxK8FD0vjdLL9eHGYEmPVCGVX0BJX04TVW9aoemsx9Yn3ZtfvmQHuROiB-GcA5wOSb-GvhzfplY09GQr7g7221MiYCHYimmEJyxLV5clWPXu6izzVLDyG9l2ewCifiuBLD0O1U_fPlahHTmidwHKJEAEn39biNw5E_dr8WyZ3xBvJa9dP50m0xeyN4COR-xlYcEbuDcKoqN6BnY0bMNDxQYlBO--QcPLQ6h48uTJszwzsmNIwHoi0xy5dQah7c9Nt2lpMuNt1Wix-O8JWYCqaiCKxjwt9G8kabMbzhp1n3LetWweoyV7qJTbiB13Byv6SZwMO9M.8j8wtvwBAHzqRhv5Ii9jjQ",
    }


@pytest.fixture
def mock_supplementary_data_payload_missing_data():
    return {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
    }


@pytest.fixture
def mock_cir_payload() -> dict:
    return {
        "mime_type": "application/json/ons/eq",
        "language": "en",
        "schema_version": "0.0.1",
        "data_version": "0.0.3",
        "survey_id": "001",
        "title": "Test mobile number",
        "theme": "default",
        "description": "A questionnaire to test a mobile number",
        "metadata": [
            {"name": "user_id", "type": "string"},
            {"name": "period_id", "type": "string"},
            {"name": "ru_name", "type": "string"},
        ],
        "questionnaire_flow": {"type": "Hub", "options": {}},
        "sections": [
            {
                "id": "default-section",
                "groups": [
                    {
                        "blocks": [
                            {
                                "type": "Question",
                                "id": "mobile-number-block",
                                "question": {
                                    "answers": [
                                        {
                                            "id": "mobile-number-answer",
                                            "label": "UK mobile Number",
                                            "mandatory": True,
                                            "type": "MobileNumber",
                                        }
                                    ],
                                    "id": "mobile-number-question",
                                    "title": "What is your mobile number?",
                                    "type": "General",
                                },
                            }
                        ],
                        "id": "group",
                    }
                ],
            }
        ],
    }
