#!/usr/bin/env bash
tag=replace-beis-with-dbt-dsit-theme
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
