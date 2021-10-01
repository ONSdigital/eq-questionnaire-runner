#!/usr/bin/env bash
tag=generate_date_range-and-format_date_range_pair
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
