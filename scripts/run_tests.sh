#!/bin/bash
#
# Run all project tests
#

set -e

echo "Starting Validator"
./scripts/run_validator.sh

echo "Running schema validation"
./scripts/validate_test_schemas.sh schemas/test/en

echo "Running python lint tests"
./scripts/run_lint_python.sh

echo "Running js lint tests"
npm run lint

echo "Running unit tests"
./scripts/run_tests_unit.sh

echo "Running functional tests"
./scripts/run_tests_functional.sh
