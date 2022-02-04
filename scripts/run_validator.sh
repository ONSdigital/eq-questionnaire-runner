#!/usr/bin/env bash
tag=conditional-trad-as
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
