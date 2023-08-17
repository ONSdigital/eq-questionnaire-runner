#!/usr/bin/env bash
tag=latest
TAG=${tag} docker-compose -f docker-compose-sds.yml up -d
