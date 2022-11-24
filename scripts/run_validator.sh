#!/usr/bin/env bash
tag=refactor-calculated-summary
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
