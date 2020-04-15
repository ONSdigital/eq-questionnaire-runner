import logging
import sys
import requests

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def get_schema_version():
    file = open("Makefile", "r")
    contents = file.readlines()
    for line in contents:
        if "onsdigital/eq-questionnaire-schemas" not in line:
            continue
        version = line.split(" ")[-1].strip()
        return version


try:
    response = requests.get(
        "https://api.github.com/repos/ONSdigital/eq-questionnaire-schemas/releases"
    )
    if response.status_code == 200:
        latest_tag = response.json()[0]["tag_name"]
        if latest_tag != get_schema_version():
            logger.error("eq-questionnaire-schemas is out of date, update makefile")
            sys.exit(1)
except RequestException:
    logger.error("Can't check eq-questionnaire-schemas release version")
