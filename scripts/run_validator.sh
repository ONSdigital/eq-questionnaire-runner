#!/usr/bin/env bash
tag=update-max-lenght-to-15-digits
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
