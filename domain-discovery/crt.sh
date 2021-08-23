#!/bin/bash
# --- 
# Searches crt.sh by specified query and retrives found urls without duplicates
# ---
curl -s -X GET https://crt.sh?q=$1 | grep -Po "(?<=<TD>)([a-zA-Z0-9./?=_%:-]*)(?=</TD>)" | sort -u
