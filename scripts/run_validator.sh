#!/usr/bin/env bash
tag=add-dbt-theme
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
