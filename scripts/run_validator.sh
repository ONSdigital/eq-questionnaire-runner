#!/usr/bin/env bash
tag=add-flag-for-ir-on-hub
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
