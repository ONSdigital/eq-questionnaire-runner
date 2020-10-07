#!/usr/bin/env bash
tag=support-for-relation-to-anyone-pattern
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
