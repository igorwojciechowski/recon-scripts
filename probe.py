#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime


def probe(subdomains_file: str, output_file: str):
    """
    Probe subdomains with httpx
    """
    subprocess.Popen(['httpx', '-l', subdomains_file],
                     stdout=open(output_file, 'a'))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("No domain provided")
        sys.exit(1)

    DOMAINS_FILE = sys.argv[1]
    DATE = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    OUTPUT_FILE = f"probe-{DATE}.txt"

    probe(DOMAINS_FILE, OUTPUT_FILE)
