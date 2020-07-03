#!/usr/bin/env bash
tag=extend-question-summary-concat-answer-types
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
