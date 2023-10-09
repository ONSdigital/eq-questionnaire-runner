#!/usr/bin/env bash
tag=add-ukhsa-ons-theme
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
