#!/usr/bin/env bash
tag=grand-calculated-summary-value-sources-fix
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
