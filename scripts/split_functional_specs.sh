#!/bin/bash
# Usage: ./scripts/split_functional_specs.sh <total_shards> <shard_number>
set -e

TOTAL_SHARDS=$1
SHARD_NUMBER=$2

SPECS=($(ls tests/functional/spec/**/*.spec.js | sort))
NUM_SPECS=${#SPECS[@]}

for i in "${!SPECS[@]}"; do
  if (( i % TOTAL_SHARDS + 1 == SHARD_NUMBER )); then
    echo "./${SPECS[$i]#tests/functional/}"
  fi
done
