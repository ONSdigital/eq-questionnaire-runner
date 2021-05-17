#!/usr/bin/env bash
tag=refactor-for-load-from-params-resolver
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
