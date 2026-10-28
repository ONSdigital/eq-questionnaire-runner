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

echo "Fetching ${DOWNLOAD_URL}"
curl -fL --url "${DOWNLOAD_URL}" --output "${TEMP_DIR}/design-system.tgz"

# Extract tarball (npm packages are rooted under "package/")
tar -xzf "${TEMP_DIR}/design-system.tgz" -C "${TEMP_DIR}"

if [ ! -d "${TEMP_DIR}/package/components" ] || [ ! -d "${TEMP_DIR}/package/layout" ]; then
	echo "Unexpected design-system tarball structure: expected package/components and package/layout"
	exit 1
fi

# Replace local template folders
rm -rf ./templates/components ./templates/layout
mkdir -p ./templates
cp -R "${TEMP_DIR}/package/components" ./templates/
cp -R "${TEMP_DIR}/package/layout" ./templates/

if [ ! -d "./templates/components" ] || [ ! -d "./templates/layout" ] || [ ! -f "./templates/layout/_template.njk" ]; then
	echo "Post-copy check failed: expected templates/components and templates/layout/_template.njk"
	exit 1
fi

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

if [ ! -d "./templates/components" ] || [ ! -d "./templates/layout" ] || [ ! -f "./templates/layout/_template.njk" ]; then
	echo "Post-copy check failed: expected templates/components and templates/layout/_template.njk"
	exit 1
fi

rm -rf "${TEMP_DIR}"
