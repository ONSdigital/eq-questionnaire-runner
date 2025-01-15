import json
import subprocess
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

error = False
passed = 0
failed = 0

def validate_schema(schema_path):
    try:
        result = subprocess.run(
            ['curl', '-s', '-w', 'HTTPSTATUS:%{http_code}', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', f'@{schema_path}',
             'http://localhost:5001/validate'],
            capture_output=True,
            text=True,
            check=True
        )
        return schema_path, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error validating schema {schema_path}: {e}")
        return schema_path, None


def main():
    file_path = './schemas/test/en'
    schemas = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.json')]

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_schema = {executor.submit(validate_schema, schema): schema for schema in schemas}
        for future in as_completed(future_to_schema):
            schema = future_to_schema[future]
            try:
                schema_path, result = future.result()
                # Extract HTTP body
                http_body = re.sub(r'HTTPSTATUS:.*', '', result)

                # Convert HTTP body to JSON
                http_body_json = json.loads(http_body)

                # Extract HTTP status code
                result_response = re.search(r'HTTPSTATUS:(\d+)', result)[1]

                if result_response == "200" and http_body_json == {}:
                    print(f"\033[32m{schema_path}: PASSED\033[0m")
                    global passed
                    passed += 1
                else:
                    print(f"\033[31m{schema_path}: FAILED")
                    print(f"HTTP Status @ /validate: {result_response}")
                    print(f"HTTP Status: {http_body_json}\033[0m")
                    global error
                    error = True
                    global failed
                    failed += 1
            except Exception as e:
                print(f"Error processing {schema}: {e}")
    if error:
        print(f"\033[32m{passed} passed\033[0m - \033[31m{failed} failed\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
