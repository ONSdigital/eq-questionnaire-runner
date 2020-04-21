#!/usr/bin/env bash
# https://gist.github.com/lukechilds/a83e1d7127b78fef38c2914c4ececc3c

set -e

get_latest_release() {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
    grep '"tag_name":' |                                            # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}

get_latest_release "onsdigital/eq-questionnaire-schemas" > .schemas-version
