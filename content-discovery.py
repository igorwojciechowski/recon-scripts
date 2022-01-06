#!/usr/bin/env python3
import sys
import subprocess
import re
from datetime import datetime
from multiprocessing import Manager, Pool
import utils
import os


def enumerate_content(url: str, wordlist: str, output_file: str) -> None:
    proc = subprocess.Popen([
        "gobuster", "dir", "-u", url, "-w", wordlist, "-o", output_file, "--wildcard"
    ],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL)
    proc.wait()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1, 'No urls file provided')

    URLS_FILE = sys.argv[1]
    try:
        WORDLIST = sys.argv[2]
    except IndexError:
        WORDLIST = f"{os.environ['PAYLOADS']}/raft-large-all.txt"
    MANAGER = Manager()
    PROCS = MANAGER.list()
    THREADS = 5
    urls = []
    results = []

    with open(URLS_FILE, 'r') as f:
        for url in f.readlines():
            urls.append(url.replace('\n', ''))

    with Pool(THREADS) as pool:
        for url in urls:
            STARTED = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            domain = re.search(r'([A-z0-9-_.]*)$', url).group(0)
            utils.make_domain_dir_structure(domain)
            directory = utils.get_directory_path(domain)
            output_file = f'{directory}/gobuster-{STARTED}.txt'
            result = pool.apply_async(enumerate_content, args=(url, WORDLIST, output_file))
            results.append(result)
        [result.wait() for result in results]
