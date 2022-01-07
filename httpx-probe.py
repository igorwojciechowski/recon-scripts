#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def probe(subdomains_file: str, output_file: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-l', subdomains_file, '-probe', '-p', '80,443,8000,8080', '-nc'],
                         stderr=subprocess.DEVNULL,
                         stdout=open(output_file, 'a'))
    p.wait()


if __name__ == '__main__':

    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('-d', '--domains', type=str, required=True)
    ARGS = ARG_PARSER.parse_args()

    DOMAINS = ARGS.domains
    DATE = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    OUTPUT_FILE = f"probe-{DATE}.txt"

    probe(DOMAINS, OUTPUT_FILE)
