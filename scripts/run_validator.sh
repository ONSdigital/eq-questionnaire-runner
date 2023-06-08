#!/usr/bin/env bash
tag=list-collector_repeating_blcoks
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
