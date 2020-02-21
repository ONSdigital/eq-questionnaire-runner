#!/usr/bin/env bash

branch=add_show_on_hub_to_section
docker pull onsdigital/eq-questionnaire-validator:$branch
docker run -d -p 5001:5000 "add_show_on_hub_to_section"
