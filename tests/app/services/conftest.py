import pytest


@pytest.fixture
def decrypted_mock_supplementary_data_payload():
    return {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "data": {
            "schema_version": "v1",
            "identifier": "12345678901",
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
        "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk2In0.tK1Duhk7FmvMn7X6QaSvrpx5U0wOzOyzFwOaLUksCBrPI2J7Tnz1mRMoQla-ekuG-B0DLaQUWA74vgN44UhWbLd7fYbIwjt9TCgdfVyP7P9tOebe55xEHsbvMmRf7F1F37KjPXXk7usDkFuuzl_fjhLwmrjNn90YA93QLy1PbGiMcC8JFYDwLL-vaWslB-VGgKEdud4LCY80xvwxzxxHYtpEQ2NpBXt9zpodwQCFqn8LHHGN80h8_-TE2gOInWccRd7GsyzvH5hGb-wxmgodJQFrPse4v6VBgTJbixMFvxulZqAyYULzU7LiFGSQZqrhqqL4-UXWRmeJX5aYR9AtzO2kGl6gVDZ2d0jGLuHwOSiJ9CLtvltKU8ai0ZfN-qUY6ZnV2lZ7wq_fZrat2-VdxE-ktMy6owGBD3DwHcd_QwAPlDFDEJeAS1G4JKuyfCb_siM5wLd1_HV_6kG2IcyAtt0usRj2D36N2K2lufJjJJlDh2QJm6r5H1pGci8AR7YCJ7nAbmlyMJ7RLJ65TswcvWT7A8jQnVBZT2NCL3_WZ9o2cGj9HixzATzVPkP54LWPTgDI-Q0-nLaBfkHFcR9-6v9f_DFW_zcj2yFfu93HRSc4GSjGs7x0dZkpY-JLFqcNzxcEeUMODUgeE9QZAIF2VsS7NcodbpqJJlOBbevJeZU.Z6Gte9FcRQfo3vos.kwL0nw0aZj6hYugPWt5oa4j-SwdBhDl-ynd6UDtqf1WFDLZcS_DBaXXT2tB7vh_zHNJaMhkJfZV4iT1jr6Wat8pDhL4c_IrclxMLagU22dST6aZcCBkVtvVUCB5dt0AO64NUBysiDf8nTnJyzLnC-pMXvc1QXSS5OMdrFdLPm3jaTAT7y1NYNtIQyRrLZj7PayRQK5w5JS3clq3BSn780rECVxM4FLuDsO0hft-feDKW700Xe4HAeXqaLwADM3bUXMeriiX2CvdTkBB2gv2uBQdR6FIVwGPDbTvXHf1bvTCLmaIT-Ki3pDh_BIrZhgg9ZO8Pft5ZEWWeQR0kF-2eglkro90AWSzUFrQO5YsYsQ-YdjoajeyyiQTg1zW3LyGM3F7-EDKrAZzUgiUhK9UC1Lfheg7Owg7aG-gYN3N6UU5ngnXegcJtNEnoULOLnck0aLS7Ku0v19tw4ObGPW28KZo.Ewzo-AyJbBMCWPqlhjhhAw",
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
