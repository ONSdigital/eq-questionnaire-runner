#!/usr/bin/env bash

branch=v3
docker pull onsdigital/eq-schema-validator:$branch
docker run -d -p 5001:5000 "onsdigital/eq-schema-validator:$branch"
