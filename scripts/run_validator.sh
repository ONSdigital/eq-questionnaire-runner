#!/usr/bin/env bash
tag=validating-dynamic-based-on-list-collector
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
