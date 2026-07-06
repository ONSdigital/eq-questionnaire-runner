import json
import logging
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_connection():
    for connection_attempts in range(4, 0, -1):
        response = subprocess.run(
            [
                "curl",
                "-so",
                "/dev/null",
                "-w",
                "%{http_code}",
                "http://localhost:5002/status",
            ],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()

        if response == "200":
            return

        logging.error("\033[31m---Error: Schema Validator Not Reachable---\033[0m")
        logging.error("\033[31mHTTP Status: %s\033[0m", response)

        if connection_attempts == 1:
            logging.info("Exiting...\n")
            sys.exit(1)

        logging.info("Retrying...\n")
        time.sleep(5)


def get_schemas() -> list[str]:
    if len(sys.argv) == 1 or sys.argv[1] == "--local":
        file_path = "./schemas/test/en"
        schemas = [
            os.path.join(file_path, f)
            for f in os.listdir(file_path)
            if f.endswith(".json")
        ]
        logging.info("--- Testing Schemas in %s ---", file_path)
    else:
        schema = sys.argv[1]
        schemas = [schema]
        logging.info("--- Testing %s Schema ---", schema)
    return schemas


def validate_schema(schema_path):
    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-w",
                "HTTPSTATUS:%{http_code}",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "-d",
                f"@{schema_path}",
                "http://localhost:5001/validate",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return schema_path, result.stdout
    except subprocess.CalledProcessError as e:
        logging.info("Error validating schema %s: %s", schema_path, e)
        return schema_path, None


def process_schema(future, future_to_schema):
    # pylint: disable=broad-exception-caught
    schema = future_to_schema[future]
    try:
        schema_path, result = future.result()
        # Extract HTTP body
        http_body = re.sub(r"HTTPSTATUS:.*", "", result)

        # Convert HTTP body to JSON
        http_body_json = json.loads(http_body)

        # Get validator_version and success values
        validator_version = http_body_json.get("validator_version")
        success = http_body_json.get("success")

        # Format JSON
        formatted_json = json.dumps(http_body_json, indent=4)

        # Extract HTTP status code
        result_response = re.search(r"HTTPSTATUS:(\d+)", result)[1]

        if "errors" not in http_body_json and all(
            [validator_version, success, result_response == "200"]
        ):
            logging.info(
                "\033[32m%s: PASSED | validator_version: %s | success: %s\033[0m",
                schema_path,
                validator_version,
                success,
            )
            return True

        logging.error(
            "\033[31m%s: FAILED | validator_version: %s | success: %s\033[0m",
            schema_path,
            validator_version,
            success,
        )
        logging.error("\033[31mHTTP Status @ /validate: %s\033[0m", result_response)
        logging.error("\033[31mHTTP Status: %s\033[0m", formatted_json)
        return False

    except Exception as e:
        logging.error("\033[31mError processing %s: %s\033[0m", schema, e)
        return False


def main():
    passed = 0
    failed = 0

    check_connection()
    schemas = get_schemas()

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_schema = {
            executor.submit(validate_schema, schema): schema for schema in schemas
        }
        for future in as_completed(future_to_schema):
            if process_schema(future, future_to_schema):
                passed += 1
            else:
                failed += 1

    logging.info("\033[32m%s passed\033[0m - \033[31m%s failed\033[0m", passed, failed)
    if passed != len(schemas):
        sys.exit(1)


if __name__ == "__main__":
    main()
