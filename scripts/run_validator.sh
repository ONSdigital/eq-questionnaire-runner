#!/usr/bin/env bash
tag=remove-default-checkbox-label
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
