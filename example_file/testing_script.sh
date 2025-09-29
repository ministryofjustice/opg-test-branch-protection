#!/bin/bash

# Wait 1 min to simulate testing of the application.
sleep 60

total=0

for file in example_file/number_*.txt; do
  if [[ -f "$file" ]]; then
    value=$(cat "$file")
    echo "Found $file with value $value"
    total=$((total + value))
  fi
done

echo "Total sum: $total"

if [ "$total" -gt 200 ]; then
  echo "Total exceeds 200, failing test"
  exit 1
else
  echo "Total is within limit, test passes"
fi
