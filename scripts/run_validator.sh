#!/usr/bin/env bash
tag=add-html-validation
TAG=${tag} docker compose -f docker-compose-schema-validator.yml up -d
