#!/bin/bash
# Usage: ./scripts/split_functional_specs.sh <shard_count> <shard>
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Error: Missing arguments. Usage: $0 <shard_count> <shard>" >&2
  exit 1
fi

if ! [[ "$1" =~ ^[0-9]+$ ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
  echo "Error: Arguments must be positive integers." >&2
  exit 1
fi

SHARD_COUNT=$1
SHARD=$2

if (( SHARD_COUNT == 0 )); then
  echo "Error: shard_count must be greater than 0." >&2
  exit 1
fi

if (( SHARD < 1 || SHARD > SHARD_COUNT )); then
  echo "Error: shard must be between 1 and $SHARD_COUNT." >&2
  exit 1
fi

mapfile -t SPECS < <(find tests/functional/spec -type f -name "*.spec.ts" | sort)

SELECTED=()
for i in "${!SPECS[@]}"; do
  if (( i % SHARD_COUNT + 1 == SHARD )); then
    SELECTED+=("tests/functional/${SPECS[$i]#tests/functional/}")
  fi
done

# Output as comma-separated list
IFS=, ; echo "${SELECTED[*]}"
