#!/usr/bin/env bash
tag=use-AJV-validator
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml  up -d
