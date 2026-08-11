#!/bin/bash
#
# Run project through linting
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_lint_python.sh

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

ruff check .
display_result $? 1 "Ruff code style check (including isort)"

./scripts/run_mypy.sh
display_result $? 1 "Mypy type check"

black --check . --exclude node_modules
display_result $? 1 "Python code formatting check"
