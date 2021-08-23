#!/bin/bash
# ---
# Wrapper for dirsearch script
# ---

if [ -t 0 ]; then
    echo "No urls provided. Exiting..."
    exit 1
fi

readarray domains

echo "Searching for dirsearch script..."
dirsearchPath=$(find / -name "dirsearch.py" -print -quit 2>/dev/null)
if [ -z "$dirsearchPath" ]; then
    echo "Could not find dirsearch script! Exiting..."
    exit 1
fi

echo "Got it! Running..."
for domain in "${domains[@]}"
do
    target=$(echo "$domain" | tr -d '\n\r')
    python3 "$dirsearchPath" -u "$target" -e "/" --xml-report "dirsearch-$target.xml" | tee "dirsearch-$target.out"
done
