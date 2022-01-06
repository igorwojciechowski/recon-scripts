#!/usr/bin/env python3
import sys
import re
import utils


if len(sys.argv) < 2:
    sys.exit(1, 'Domains file not provided')

DOMAINS = sys.argv[1]


with open(DOMAINS, 'r') as domains_file:
    for url in domains_file.readlines():
        domain = re.search(r'([A-z0-9-_.]*)$', url).group(0)
        utils.make_domain_dir_structure(domain)
