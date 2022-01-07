#!/usr/bin/env python3
import subprocess
import re
from datetime import datetime
from multiprocessing import Manager, Pool
import utils
import os
import argparse


def enumerate_content(url: str, wordlist: str, output_file: str, *args) -> None:
    proc = subprocess.Popen([
        "gobuster", "dir", "-u", url, "-w", wordlist, "-o", output_file, "--wildcard", *args
    ],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL)
    proc.wait()


if __name__ == '__main__':
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('-u', '--urls', type=str, required=True)
    ARG_PARSER.add_argument('-w', '--wordlist', type=str, default=f"{os.environ['PAYLOADS']}/raft-large-all.txt", help="wordlist")
    ARG_PARSER.add_argument('-c', '--concurrency', type=int, default=5, help="Number of max parallel gobuster processes")
    ARGS = ARG_PARSER.parse_args()

    URLS_FILE = ARGS.urls
    WORDLIST = ARGS.wordlist
    CONCURRENCY = ARGS.concurrency

    MANAGER = Manager()
    PROCS = MANAGER.list()

    urls = []
    results = []

    with open(URLS_FILE, 'r') as f:
        for url in f.readlines():
            urls.append(url.replace('\n', ''))

    with Pool(CONCURRENCY) as pool:
        for url in urls:
            STARTED = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            domain = re.search(r'([A-z0-9-_.]*)$', url).group(0)
            utils.make_domain_dir_structure(domain)
            directory = utils.get_directory_path(domain)
            output_file = f'{directory}/gobuster-{STARTED}.txt'
            result = pool.apply_async(enumerate_content, args=(url, WORDLIST, output_file))
            results.append(result)
        [result.wait() for result in results]
