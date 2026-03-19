#!/usr/bin/env bash
tag=348-merge
TAG=${tag} docker compose -f docker-compose-schema-validator.yml pull
TAG=${tag} docker compose -f docker-compose-schema-validator.yml up -d
