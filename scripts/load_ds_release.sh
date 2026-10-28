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

# Replace local template folders
rm -rf ./templates/components ./templates/layout
mkdir -p ./templates
cp -R "${TEMP_DIR}/package/components" ./templates/
cp -R "${TEMP_DIR}/package/layout" ./templates/

rm -rf "${TEMP_DIR}"
