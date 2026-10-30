#!/usr/bin/env bash

set -eu

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "${DIR}"/.. || exit

if [ "$#" -ne 1 ]; then
	echo "Usage: load_ds_release.sh {RELEASE}"
	exit 1
fi

RELEASE="$1"

DOWNLOAD_URL="https://registry.npmjs.org/@ons/design-system/-/design-system-${RELEASE}.tgz"
TEMP_DIR=$(mktemp -d)
PRINT_CSS_DIR="${PRINT_STYLE_SHEET_FILE_PATH:-templates/assets/styles}"

echo "Fetching ${DOWNLOAD_URL}"
curl -fL --url "${DOWNLOAD_URL}" --output "${TEMP_DIR}/design-system.tgz"

# Extract tarball (npm packages are rooted under "package/")
tar -xzf "${TEMP_DIR}/design-system.tgz" -C "${TEMP_DIR}"

# Copy template folders
cp -R "${TEMP_DIR}/package/components" ./templates/
cp -R "${TEMP_DIR}/package/layout" ./templates/

# Copy print.css to use with pdf generation
mkdir -p "./${PRINT_CSS_DIR}"
cp "${TEMP_DIR}/package/css/print.css" "./${PRINT_CSS_DIR}/print.css"

# Set release_version required by the design-system template so asset URLs resolve correctly and match the previous templates.zip output.
# Remove any existing release_version line first to keep this step idempotent.
TEMPLATE_FILE="./templates/layout/_template.njk"
if [ -f "${TEMPLATE_FILE}" ]; then
	TMP_TEMPLATE=$(mktemp)
	{
		echo "{% set release_version = '${RELEASE}' %}"
		grep -vE "^\{% set release_version = '.*' %\}$" "${TEMPLATE_FILE}"
	} > "${TMP_TEMPLATE}"
	mv "${TMP_TEMPLATE}" "${TEMPLATE_FILE}"
fi

rm -rf "${TEMP_DIR}"
