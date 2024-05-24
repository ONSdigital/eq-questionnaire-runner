#!/usr/bin/env bash
tag=add-nhse-theme
TAG=${tag} docker compose -f docker-compose-schema-validator.yml up -d
