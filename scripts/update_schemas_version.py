import sys
from fileinput import FileInput

import requests

from requests.exceptions import RequestException


try:
    response = requests.get(
        "https://api.github.com/repos/ONSdigital/eq-questionnaire-schemas/releases"
    )
    if response.status_code == 200:
        latest_tag = response.json()[0]["tag_name"]
        file = open("Makefile", "r")
        for line in file:
            if "onsdigital/eq-questionnaire-schemas" not in line:
                continue
            version = line.split(" ")[-1].strip()
            line.replace(version, latest_tag)
        file.close()
        with FileInput("Makefile", inplace=True) as file:
            for line in file:
                print(line.replace(version, latest_tag), end='')
        file.close()
    else:
        sys.exit(1)
except RequestException:
    sys.exit(1)
