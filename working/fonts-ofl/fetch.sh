#!/usr/bin/env bash
# Fetch complete OFL font families from the google/fonts repository (unsubsetted,
# all OpenType features intact). For internal audition only — never packaged.
set -e
for dir in "$@"; do
  mkdir -p "$dir"
  meta=$(curl -fsS "https://raw.githubusercontent.com/google/fonts/main/ofl/$dir/METADATA.pb") || { echo "MISS $dir"; continue; }
  echo "$meta" > "$dir/METADATA.pb"
  for f in $(echo "$meta" | grep -oP 'filename: "\K[^"]+' | sort -u); do
    enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")
    curl -fsS -o "$dir/$f" "https://raw.githubusercontent.com/google/fonts/main/ofl/$dir/$enc" && echo "ok $dir/$f" || echo "fail $dir/$f"
  done
  curl -fsS -o "$dir/OFL.txt" "https://raw.githubusercontent.com/google/fonts/main/ofl/$dir/OFL.txt" || true
done
