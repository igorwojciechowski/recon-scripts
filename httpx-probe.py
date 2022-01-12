#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def probe(subdomains_file: str):
    """
    Probe subdomains with httpx
    """
    p = subprocess.Popen(['httpx', '-l', subdomains_file, '-probe', '-p', '80,443,8000,8080', '-nc', '-sc', '-cl'],
                         stderr=subprocess.DEVNULL,
                         stdout=subprocess.PIPE)
    p.wait()
    return p.stdout


def outputToFile(output_file: str, data: list):
    with open(output_file, 'a') as _file:
        _file.write(''.join(data))



if __name__ == '__main__':

    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('-d', '--domains', type=str, required=True)
    ARGS = ARG_PARSER.parse_args()

    DOMAINS = ARGS.domains
    DATE = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    OUTPUT_FILE = f"probe-{DATE}.txt"

    stdout = probe(DOMAINS)
    output = [_.decode() for _ in stdout.readlines()]

    

