#!/bin/bash
# Usage: ./scripts/split_functional_specs.sh <total_shards> <shard_number>
set -e

TOTAL_SHARDS=$1
SHARD_NUMBER=$2

mapfile -t SPECS < <(find tests/functional/spec -type f -name "*.spec.js" | sort)

SELECTED=()
for i in "${!SPECS[@]}"; do
  if (( i % TOTAL_SHARDS + 1 == SHARD_NUMBER )); then
    SELECTED+=("${SPECS[$i]}")
  fi
done

# Output as comma-separated list
IFS=, ; echo "${SELECTED[*]}"
