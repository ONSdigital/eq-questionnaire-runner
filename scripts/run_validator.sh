#!/usr/bin/env bash
tag=add-dynamic-options-identifier-check
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
