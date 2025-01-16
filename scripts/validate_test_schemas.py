import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

error = False
passed = 0
failed = 0


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
        print(f"Error validating schema {schema_path}: {e}")
        return schema_path, None


def main():
    # pylint: disable=global-statement, broad-exception-caught
    checks = 4

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
            print("\033[31m---Error: Schema Validator Not Reachable---\033[0m")
            print(f"\033[31mHTTP Status: {response}\033[0m")
            if checks != 1:
                print("Retrying...\n")
                time.sleep(5)
            else:
                print("Exiting...\n")
                sys.exit(1)
            checks -= 1
        else:
            checks = 0

    if len(sys.argv) == 1 or sys.argv[1] == "--local":
        file_path = "./schemas/test/en"
    else:
        file_path = sys.argv[1]

    print(f"--- Testing Schemas in {file_path} ---")

    schemas = [
        os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith(".json")
    ]

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

                # Extract HTTP status code
                result_response = re.search(r"HTTPSTATUS:(\d+)", result)[1]

                if result_response == "200" and http_body_json == {}:
                    print(f"\033[32m{schema_path}: PASSED\033[0m")
                    global passed
                    passed += 1
                else:
                    print(f"\033[31m{schema_path}: FAILED\033[0m")
                    print(f"\033[31mHTTP Status @ /validate: {result_response}\033[0m")
                    print(f"\033[31mHTTP Status: {http_body_json}\033[0m")
                    global error, failed
                    error = True
                    failed += 1
            except Exception as e:
                print(f"\033[31mError processing {schema}: {e}\033[0m")
    if error:
        print(f"\033[32m{passed} passed\033[0m - \033[31m{failed} failed\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
