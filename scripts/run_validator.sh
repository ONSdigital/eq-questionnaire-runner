#!/usr/bin/env bash

branch=age_confirmation_playback
docker pull onsdigital/eq-questionnaire-validator:$branch
docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$branch"
