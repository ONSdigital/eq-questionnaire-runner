#!/usr/bin/env bash

run_docker=true
if [ "$1" == "--local" ] || [ "$2" == "--local" ]; then
    run_docker=false
fi

if [ "$run_docker" == true ]; then
    branch=v3
    docker pull onsdigital/eq-schema-validator:$branch
    validator="$(docker run -d -p 5001:5000 onsdigital/eq-schema-validator:$branch)"
    sleep 3
fi
