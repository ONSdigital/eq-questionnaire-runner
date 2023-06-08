#!/usr/bin/env bash
tag=list-collector-repeating-blocks
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
