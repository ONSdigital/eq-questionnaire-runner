#!/usr/bin/env bash

branch=add_list_section_summary_type
docker pull onsdigital/eq-schema-validator:$branch
docker run -d -p 5001:5000 "onsdigital/eq-schema-validator:$branch"
