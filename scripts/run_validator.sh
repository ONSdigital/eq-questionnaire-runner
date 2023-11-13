#!/usr/bin/env bash
tag=remove-census-survey-configs
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
