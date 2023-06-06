#!/usr/bin/env bash
tag=feat-looping-4
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
