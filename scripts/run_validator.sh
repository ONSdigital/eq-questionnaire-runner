#!/usr/bin/env bash
tag=block-and-non-block-page-titles
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
