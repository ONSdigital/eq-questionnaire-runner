#!/usr/bin/env bash
tag=fix-format-unit-calculated-summary-source
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
