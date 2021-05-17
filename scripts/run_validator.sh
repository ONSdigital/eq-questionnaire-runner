#!/usr/bin/env bash
tag=introduce-questionnaire-flow
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
