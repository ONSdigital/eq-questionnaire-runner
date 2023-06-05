# Running the Mock SDS endpoint

In order to test loading supplementary data, we have a development script that creates a Mock SDS endpoint in Flask that
returns mocked supplementary data.

Ensure the following env var is set before running the script:
```bash
SDS_API_BASE_URL=http://localhost:5003/v1/unit_data
```

From the home directory, run using
```python
 python -m scripts.mock_sds_endpoint
```

The following datasets are available using the mocked endpoint. To retrieve the data, one of the following dataset IDs needs to be set using the `sds_dataset_id`
field in Launcher.

| Dataset ID             | Description                                                |
|------------------------|------------------------------------------------------------|
| `c067f6de-6d64-42b1-8b02-431a3486c178` | Basic supplementary data structure with no repeating items |
| `34a80231-c49a-44d0-91a6-8fe1fb190e64`  | Supplementary data structure with repeating items          |

