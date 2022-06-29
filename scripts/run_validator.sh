#!/usr/bin/env bash
tag=add-qcode-validation
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
