#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "${DIR}"/.. || exit

SCHEMAS_VERSION="v0.0.1"

TEMP_DIR=$(mktemp -d)

curl -L --url "https://github.com/ONSdigital/eq-questionnaire-schemas/releases/download/$SCHEMAS_VERSION/schemas.zip" --output "${TEMP_DIR}/schemas.zip"
unzip "${TEMP_DIR}/schemas.zip" -d ./
rm -rf "${TEMP_DIR}"

