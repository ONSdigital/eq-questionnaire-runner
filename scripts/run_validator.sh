#!/usr/bin/env bash
tag=support-supplementary-lists-property
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
