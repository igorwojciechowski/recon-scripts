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


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--urls', type=str, required=True)
    args = arg_parser.parse_args()

    urls_file = args.urls
    date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    output_directory = f"aquatone-{date}"

    with open(urls_file, 'r') as _file:
        payload = [_.replace("\n", "") for _ in _file.readlines()]
    aquatone(payload, output_directory)


if __name__ == '__main__':
    main()
