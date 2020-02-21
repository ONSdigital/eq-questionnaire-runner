#!/usr/bin/env bash

checks=4
branch=custom-section-summaries

until [ "$checks" == 0 ]; do
    response="$(curl -so /dev/null -w '%{http_code}' http://localhost:5001/status)"

    if [ "$response" != "200" ]; then
        echo "Starting Schema Validator"
        docker pull onsdigital/eq-questionnaire-validator:$branch
        docker run -d -p 5001:5000 "onsdigital/eq-questionnaire-validator:$branch"
        if [ "$checks"  != 1 ]; then
            echo -e "Retrying...${default}\\n"
            sleep 5
        else
            echo -e "Exiting...${default}\\n"
            exit 1
        fi
        (( checks-- ))
    else
        echo "Schema Validator Running"
        (( checks=0 ))
    fi

done

exit 0
