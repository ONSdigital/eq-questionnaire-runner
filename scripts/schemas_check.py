import logging
import re
import requests

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

try:
    response = requests.get(
        "https://api.github.com/repos/ONSdigital/eq-questionnaire-schemas/releases"
    )
    if response.status_code == 200:
        latest_tag = response.json()[0]["tag_name"]
        f = open("Makefile", "r")
        file = f.readlines()
        for i, line in enumerate(file):
            if "onsdigital/eq-questionnaire-schemas" in line:
                ref = re.compile(r"v\d.\d.\d")
                mo = ref.search(file[i])
                version = mo.group()
                break
        if latest_tag != version:
            logger.error("eq-questionnaire-schemas is out of date, update makefile")

except RequestException:
    logger.error("Can't check eq-questionnaire-schemas release version")
