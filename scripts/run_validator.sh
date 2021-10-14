#!/usr/bin/env bash
tag=remove-skip-conditions-from-question-definition
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
