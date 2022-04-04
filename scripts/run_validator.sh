#!/usr/bin/env bash
tag="calculated-summary-value-source"
TAG=${tag} docker-compose -f docker-compose-schema-validator.yml up -d
