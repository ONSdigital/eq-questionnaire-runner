#!/usr/bin/env bash
tag=make-ajv-configurable
TAG=${tag} docker compose -f docker-compose-schema-validator.yml up -d
