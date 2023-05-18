#!/usr/bin/env bash
tag=grand-calculated-summary-validation
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
