#!/bin/bash
# ---
# Wrapper for ffuf
# ---

if [ -t 0 ]; then
    echo "No urls provided. Exiting..."
    exit 1
fi

if [ -z "$1" ]; then
  echo "No wordlist provided. Exiting..."
  exit 1
fi

readarray domains
for domain in "${domains[@]}"
do
    target=$(echo "$domain" | tr -d '\n\r')
    hostname=$(echo "$target" | grep -oP "(?<=://)(.*)(?=:\d*)")
    port=$(echo "$target" | grep -oP "(?<=:)(\d*)")

    if [ $port = 443 ] ; then
      target="https://$hostname"
    elif [ $port = 80 ] ; then
      target="http://$hostname"
    else
      target="http://$hostname:$port"
    fi
    ffuf -u "$target/FUZZ" -r -w "$1" -of html -o "$2$hostname:$port.html" -or | tee "$2$hostname:$port.txt"
done
