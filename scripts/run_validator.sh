#!/usr/bin/env bash
tag=unit-types-update
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
