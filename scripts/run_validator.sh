#!/usr/bin/env bash
tag=extend-address-answer-type-for-lookups
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
