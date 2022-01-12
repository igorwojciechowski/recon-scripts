#!/usr/bin/env python3
import argparse
import subprocess
from datetime import datetime


def aquatone(urls: str, output_directory: str):
    p = subprocess.Popen(['aquatone', '-out', output_directory],
                         stdin=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL)
    p.communicate(input='\n'.join(urls).encode())
    p.wait()


if __name__ == '__main__':

    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('-u', '--urls', type=str, required=True)
    ARGS = ARG_PARSER.parse_args()

    ULRS_FILE = ARGS.urls
    DATE = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    OUTPUT_DIRECTORY = f"aquatone-{DATE}"

    with open(ULRS_FILE, 'r') as _file:
        payload = [_.replace("\n", "") for _ in _file.readlines()]
    aquatone(payload, OUTPUT_DIRECTORY)
