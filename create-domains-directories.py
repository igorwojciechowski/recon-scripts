#!/usr/bin/env python3
import sys
import os
import utils


if len(sys.argv) < 2:
    sys.exit(1, 'Domains file not provided')

DOMAINS = sys.argv[1]


def get_domain_from_url(url: str) -> str:
    return url.split("://")[1].split(":")[0]


with open(DOMAINS, 'r') as domains_file:
    for url in domains_file.readlines():
        domain = get_domain_from_url(url.replace("\n", ""))
        utils.make_domain_dir_structure(domain)
        directory = utils.get_directory_path(domain)
        md_file = f"{directory}/{domain}.md"
        if not os.path.isfile(md_file):
            with open(md_file, 'w') as _file:
                subs = domain.split('.')
                _file.write(f"# {subs[0]}.[[{'.'.join(subs[1:])}]]")
