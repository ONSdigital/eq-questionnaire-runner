#!/usr/bin/env bash
tag=supplementary-data-value-source
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
