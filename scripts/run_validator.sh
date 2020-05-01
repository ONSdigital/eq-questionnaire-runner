#!/usr/bin/env bash

# https://github.com/ONSdigital/eq-questionnaire-validator/commit/ef9e236d8428a5661f7e7501323cc29bcf313e4c
tag=allow-multiple-list-collectors
docker pull onsdigital/eq-questionnaire-validator:$tag
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$tag"
