#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def probe(subdomains_file: str, output: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-l', subdomains_file, '-probe', '-p', '80,443,8000,8080', '-nc', '-sc', '-cl', '-retries', '0'],
                         stderr=subprocess.DEVNULL,
                         stdout=open(output, 'a'))
    p.wait()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--domains', type=str, required=True)
    args = arg_parser.parse_args()

    domains = args.domains
    date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    output_file = f"probe-{date}.txt"

    probe(domains, output_file)
