#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def probe(subdomains_file: str, output: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-l', subdomains_file, '-probe', '-p', '80,443,8000,8080', '-nc', '-sc', '-cl', '-title', '-retries', '0'],
                         stderr=subprocess.DEVNULL,
                         stdout=open(output, 'a'))
    p.wait()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--domains', type=str, required=True)
    arg_parser.add_argument('-o', '--output', type=str)
    args = arg_parser.parse_args()
    domains = args.domains
    date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    output_file = args.output if args.output else f"probe-{date}.txt"
    probe(domains, output_file)


if __name__ == '__main__':
    main()
