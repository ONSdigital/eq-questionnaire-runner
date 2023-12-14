#!/usr/bin/env bash
tag=prevent-duplicate-answer-ids-across-different-list-colectors
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
