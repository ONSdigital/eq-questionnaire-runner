import subprocess
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

error = False


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
                if result == "{}HTTPSTATUS:200":
                    print(f"Result for {schema_path}: PASSED")
                else:
                    global error
                    error = True
            except Exception as e:
                print(f"Error processing {schema}: {e}")
    if error:
        print("Some schemas failed validation")
        sys.exit(1)


if __name__ == "__main__":
    main()
