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


def main():
    # pylint: disable=broad-exception-caught, too-many-locals
    checks = 4
    error = False
    passed = 0
    failed = 0

    while checks > 0:
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

        if response != "200":
            logging.error("\033[31m---Error: Schema Validator Not Reachable---\033[0m")
            logging.error(f"\033[31mHTTP Status: {response}\033[0m")
            if checks != 1:
                logging.info("Retrying...\n")
                time.sleep(5)
            else:
                logging.info("Exiting...\n")
                sys.exit(1)
            checks -= 1
        else:
            checks = 0

    if len(sys.argv) == 1 or sys.argv[1] == "--local":
        file_path = "./schemas/test/en"
        schemas = [
            os.path.join(file_path, f)
            for f in os.listdir(file_path)
            if f.endswith(".json")
        ]
        logging.info("--- Testing Schemas in %s ---", file_path)
    else:
        file_path = sys.argv[1]
        schemas = [sys.argv[1]]
        logging.info("--- Testing %s Schema ---", file_path)

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_schema = {
            executor.submit(validate_schema, schema): schema for schema in schemas
        }
        for future in as_completed(future_to_schema):
            schema = future_to_schema[future]
            try:
                schema_path, result = future.result()
                # Extract HTTP body
                http_body = re.sub(r"HTTPSTATUS:.*", "", result)

                # Convert HTTP body to JSON
                http_body_json = json.loads(http_body)

                # Format JSON
                formatted_json = json.dumps(http_body_json, indent=4)

                # Extract HTTP status code
                result_response = re.search(r"HTTPSTATUS:(\d+)", result)[1]

                if result_response == "200" and http_body_json == {}:
                    logging.info("\033[32m%s: PASSED\033[0m", schema_path)
                    passed += 1
                else:
                    logging.error("\033[31m%s: FAILED\033[0m", schema_path)
                    logging.error(
                        "\033[31mHTTP Status @ /validate: %s\033[0m", result_response
                    )
                    logging.error("\033[31mHTTP Status: %s\033[0m", formatted_json)
                    error = True
                    failed += 1
            except Exception as e:
                logging.error("\033[31mError processing %s: {e}\033[0m", schema)

    logging.info("\033[32m%s passed\033[0m - \033[31m%s failed\033[0m", passed, failed)
    if error:
        sys.exit(1)


if __name__ == "__main__":
    main()
