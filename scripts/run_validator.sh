#!/usr/bin/env bash
tag=fast-api-conversion
TAG=${tag} docker compose -f docker-compose-schema-validator.yml up -d
