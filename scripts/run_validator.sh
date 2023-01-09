#!/usr/bin/env bash
tag=preview-question-rules
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
