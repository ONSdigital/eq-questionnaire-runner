#!/usr/bin/env bash
tag=update-validator-for-only-one-question-definition
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
