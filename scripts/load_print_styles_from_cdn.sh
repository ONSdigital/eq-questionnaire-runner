#!/usr/bin/env bash

set -e

if [ -z ${1+x} ]; then
  echo "The design system version must be passed in as an argument."
  echo "Usage: load_print_styles_from_cdn.sh {DESIGN_SYSTEM_VERSION}"
  exit 1
fi

CDN_URL=${CDN_URL:-"https://cdn.eq.gcp.onsdigital.uk"}
PRINT_STYLE_SHEET_FILE_PATH_PATH=${PRINT_STYLE_SHEET_FILE_PATH_PATH:-"templates/assets/styles"}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "${DIR}"/.. || exit

echo "Loading print style sheets from CDN for DS Version ${1}"

PATH_TO_FETCH="${CDN_URL}/design-system/${1}/css/print.css"

mkdir -p "${PRINT_STYLE_SHEET_FILE_PATH_PATH}"
FILE_LOCATION="${PRINT_STYLE_SHEET_FILE_PATH_PATH}/print.css"

curl --compressed "${PATH_TO_FETCH}" > "${FILE_LOCATION}"

echo "Saved print CSS into ${FILE_LOCATION}"
