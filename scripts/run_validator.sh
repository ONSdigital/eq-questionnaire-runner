#!/usr/bin/env bash
tag=validate-answer-label-when-multiple
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
