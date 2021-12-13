#!/usr/bin/env bash
tag=answer-labels-as-placeholders
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
