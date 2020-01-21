#!/bin/bash
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_travis.sh

set -e

echo "Starting Validator"
./scripts/run_validator.sh

echo "Running schema validation"
./scripts/validate_test_schemas.sh

echo "Running translation tests"
python -m scripts.extract_translation_templates --test

echo "Running python lint tests"
./scripts/run_lint_python.sh

echo "Running js lint tests"
yarn lint

echo "Running unit tests"
./scripts/run_tests_unit.sh

echo "Running Docker compose"
docker-compose --version
docker-compose up --build -d

echo "Running Functional tests"
./scripts/run_tests_functional.sh

echo "Stopping Docker compose"
docker-compose kill
