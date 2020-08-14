#!/usr/bin/env bash
tag=add-answer-action-for-lists
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
