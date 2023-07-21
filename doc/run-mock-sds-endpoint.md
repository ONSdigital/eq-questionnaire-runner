# Running the Mock SDS endpoint

In order to test loading supplementary data, we have a development script that creates a Mock SDS endpoint in Flask that
returns mocked supplementary data and mock dataset metadata for that supplementary data.

Ensure the following env var is set before running the script:

```bash
SDS_API_BASE_URL=http://localhost:5003
```

From the home directory, run using

```bash
python -m scripts.mock_sds_endpoint
```

The following datasets are available using the mocked endpoint. On selecting a survey that supports supplementary data,
an `sds_dataset_id` dropdown will be shown in the metadata, and if you set the `survey_id` to `123`, it will be
populated with the following options.

| Dataset ID                             | Description                                                  |
|----------------------------------------|--------------------------------------------------------------|
| `c067f6de-6d64-42b1-8b02-431a3486c178` | Basic supplementary data structure with no repeating items   |
| `34a80231-c49a-44d0-91a6-8fe1fb190e64` | Supplementary data structure with repeating items            |
| `6b378962-f0c7-4e8c-947e-7d24ee1b6b88` | Supplementary data structure with additional repeating items |

