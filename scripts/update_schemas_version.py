import sys
import logging

import requests

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

try:
    response = requests.get(
        "https://api.github.com/repos/ONSdigital/eq-questionnaire-schemas/releases/latest"
    )
    if response.status_code == 200:
        latest_tag = response.json()["tag_name"]
        file = open("schemas_version.txt", "w")
        file.write(latest_tag)
        file.close()
    else:
        logger.error("Can't check schemas version")
        sys.exit(1)
except RequestException:
    logger.error("Can't check schemas version")
    sys.exit(1)
