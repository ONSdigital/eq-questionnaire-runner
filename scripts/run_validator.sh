#!/usr/bin/env bash
tag=latest
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
