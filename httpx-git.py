#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def probe(urls: str, output_file: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-sc', '-cl', '-nc', '-fc', '403'],
                         stdin=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         stdout=open(output_file, 'a'))
    p.communicate(input='\n'.join(urls).encode())
    p.wait()


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--urls', type=str, required=True)
    args = arg_parser.parse_args()

    urls_file = args.urls
    date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    output_file = f"probe-git-{date}.txt"

    paths = [
        '.git/config',
        '.git/HEAD'
    ]

    payload = []

    with open(urls_file, 'r') as _file:
        urls = [url.replace('\n', '') for url in _file.readlines()]
        for url in urls:
            for path in paths:
                payload.append(f"{url}/{path}")
    probe(payload, output_file)
