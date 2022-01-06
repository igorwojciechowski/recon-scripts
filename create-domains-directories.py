#!/usr/bin/env python3
import sys
import os
import re
import utils


if len(sys.argv) < 2:
    sys.exit(1, 'Domains file not provided')

DOMAINS = sys.argv[1]


with open(DOMAINS, 'r') as domains_file:
    for url in domains_file.readlines():
        domain = re.search(r'([A-z0-9-_.]*)$', url).group(0)
        utils.make_domain_dir_structure(domain)
        directory = utils.get_directory_path(domain)
        md_file = f"{directory}/{domain}.md"
        if not os.path.isfile(md_file):
            with open(md_file, 'w') as _file:
                subs = domain.split('.')
                _file.write(f"# {subs[0]}.[[{'.'.join(subs[1:])}]]")

