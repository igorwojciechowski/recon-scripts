#!/usr/bin/env python3
import argparse
import re
import requests


def crtsh(domain: str):
    response = requests.get(f"https://crt.sh/?q=%25.{domain}")
    pattern = f"[A-z0-9_\-]{{1,}}\.{domain}"
    found = re.findall(pattern, response.content.decode())
    return set(found)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--domain', type=str, required=True)
    arg_parser.add_argument('-o', '--output', type=str)
    args = arg_parser.parse_args()
    domains = crtsh(args.domain)

    output = '\n'.join(domains)

    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(output)

    print(output)


if __name__ == '__main__':
    main()
