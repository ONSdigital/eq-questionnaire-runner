#!/usr/bin/env bash

green="$(tput setaf 2)"
red="$(tput setaf 1)"
default="$(tput sgr0)"
checks=4




until [ "$checks" == 0 ]; do
    response="$(curl -so /dev/null -w '%{http_code}' http://localhost:5002/status)"

    if [ "$response" != "200" ]; then
        echo "${red}---Error: Schema Validator Not Reachable---"
        echo "HTTP Status: $response"
        if [ "$checks"  != 1 ]; then
            echo -e "Retrying...${default}\\n"
            sleep 5
        else
            echo -e "Exiting...${default}\\n"
            exit 1
        fi
        (( checks-- ))
    else
        (( checks=0 ))
    fi

done

exit=0

if [ $# -eq 0 ] || [ "$1" == "--local" ]; then
    file_path="./schemas/test/en"
else
    file_path="$1"
fi

echo "--- Testing Schemas in $file_path ---"
failed=0
passed=0

file_path_name=$(find "$file_path" -name '*.json')

validate() {
    schema=$1
    result="$(curl -s -w 'HTTPSTATUS:%{http_code}' -X POST -H "Content-Type: application/json" -d @"$schema" http://localhost:5001/validate | tr -d '\n')"
    # shellcheck disable=SC2001
    HTTP_BODY=$(echo "${result}" | sed -e 's/HTTPSTATUS\:.*//g')
    result_response="${result//*HTTPSTATUS:/}"
    result_body=$(echo "$HTTP_BODY"  | python -m json.tool)

    if [ "$result_response" == "200" ] && [ "$result_body" == "{}" ]; then
        echo -e "${green}$schema - PASSED${default}"
        (( passed++ ))
    else
        echo -e "\\n${red}$schema - FAILED"
        echo "HTTP Status @ /validate: [$result_response]"
        echo -e "Error: [$result_body]${default}\\n"
        (( failed++ ))
        exit=1
    fi
}


N_TIMES_IN_PARALLEL=20

for schema in ${file_path_name}; do
   ((i=i%N_TIMES_IN_PARALLEL)); ((i++==0)) && wait
#  Spawn multiple (N_TIMES_IN_PARALLEL) processes in subshells and send to background, but keep printing outputs.
   validate "$schema" &
done



exit "$exit"
