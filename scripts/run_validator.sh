#!/usr/bin/env bash
tag=introduction_guidance
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
