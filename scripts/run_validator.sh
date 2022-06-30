#!/usr/bin/env bash
tag=allow-radios-as-mutually-exclusive-answers
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
