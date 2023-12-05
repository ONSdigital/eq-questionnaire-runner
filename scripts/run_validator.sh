#!/usr/bin/env bash
tag=grand-calculated-summary-dependencies
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
