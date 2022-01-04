#!/usr/bin/env python3
import sys
import re
import utils

if len(sys.argv) < 2:
    sys.exit(1, 'Domains file not provided')

DOMAINS = sys.argv[1]


with open(DOMAINS, 'r') as domains_file:
    for domain in domains_file.readlines():
        directory_name = re.search('(?<=://)(.*)', domain).group(0)
        utils.mkdir(directory_name)