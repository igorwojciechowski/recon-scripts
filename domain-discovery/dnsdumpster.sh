#!/bin/bash
# ---
# Queries dnsdumpster.com to find subdomains related to given domain
# ---

if [ -z $1 ]; then
    echo "Missing domain arg!"
    exit 1
fi

response=$(curl -s -i -L dnsdumpster.com)
csrftoken=$(echo "$response" | grep -oP "(?<=set-cookie: csrftoken=).+?(?=;)")
csrfmiddlewaretoken=$(echo "$response" | grep -oP "(?<=name=\"csrfmiddlewaretoken\" value=\")(.*)(?=\")")
output=$(curl -s -X POST https://dnsdumpster.com -H "Referer:https://dnsdumpster.com" -b "csrftoken=$csrftoken" -d "csrfmiddlewaretoken=$csrfmiddlewaretoken&targetip=$1")
domains=($(echo "$output" | grep -oP "(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}.$1"))

printf '%s\n' "${domains[@]}"