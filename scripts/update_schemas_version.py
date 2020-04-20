import sys
import logging

import requests

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

try:
    response = requests.get(
        "https://api.github.com/repos/ONSdigital/eq-questionnaire-schemas/releases/latest"
    )
    if response.status_code != 200:
        raise RequestException(f"Got a {response.status_code} status code.")
    latest_tag = response.json()["tag_name"]
    file = open(".schemas-version", "w")
    file.write(latest_tag)
    file.close()

except RequestException as ex:
    logger.error("Can't check schemas version - %s." % ex)
    sys.exit(1)
