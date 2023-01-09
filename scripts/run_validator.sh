#!/usr/bin/env bash
tag=preview-questions
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
