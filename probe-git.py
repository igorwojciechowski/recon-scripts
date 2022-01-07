#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime


def probe(urls: str, output_file: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-sc', '-cl', '-nc'],
                     stdin=subprocess.PIPE,
                     stdout=open(output_file, 'a'))
    p.communicate(input='\n'.join(urls).encode())              


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("No domain provided")
        sys.exit(1)

    ULRS_FILE = sys.argv[1]
    DATE = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    OUTPUT_FILE = f"probe-git-{DATE}.txt"

    PATHS = [
        '.git/config',
        '.git/HEAD'
    ]

    payload = []

    with open(ULRS_FILE, 'r') as _file:
        URLS = [url.replace('\n', '') for url in _file.readlines()]
        for url in URLS:
            for path in PATHS:
                payload.append(f"{url}/{path}")
    probe(payload, OUTPUT_FILE)
