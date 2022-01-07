#!/usr/bin/env python3
import subprocess
from datetime import datetime
from multiprocessing import Pool
import utils
import os
import argparse


def enumerate_content(urls: list, output_file: str) -> None:
    proc = subprocess.Popen(["httpx", "-sc", "-cl", "-nc", "-retries", "0", "-fc", "404"],
                            stdin=subprocess.PIPE,
                            stderr=subprocess.DEVNULL,
                            stdout=open(output_file, 'a'))
    proc.communicate(input="\n".join(urls).encode())
    proc.wait()


def prepare_payload(url: str, words: list) -> list:
    nl = '\n'
    return [f"{url}/{word.replace(nl, '')}" for word in words]


def get_url_parts(url: str) -> tuple:
    part1 = url.split("://")
    protocol = part1[0]
    part2 = part1[1].split(":")
    domain = part2[0]
    try:
        port = part2[1]
    except IndexError:
        port = "443" if protocol == "https" else "80"
    return protocol, domain, port


if __name__ == '__main__':
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('-u', '--urls', type=str, required=True)
    ARG_PARSER.add_argument('-w', '--wordlist', type=str,
                            help="wordlist", required=True)
    ARG_PARSER.add_argument('-c', '--concurrency', type=int,
                            default=5, help="Number of max parallel httpx processes")
    ARG_PARSER.add_argument('-si', '--start_index', type=int, default=0, help="Start index")
    ARG_PARSER.add_argument('-ei', '--end_index', type=int)
    ARGS = ARG_PARSER.parse_args()

    URLS_FILE = ARGS.urls
    WORDLIST = ARGS.wordlist
    CONCURRENCY = ARGS.concurrency

    urls = []
    words = []
    results = []

    
    with open(URLS_FILE, 'r') as _file:
        START_INDEX = ARGS.start_index
        END_INDEX = ARGS.end_index if ARGS.end_index else len(_file.readlines())
        urls = [_.replace("\n", "") for _ in _file.readlines()[START_INDEX:END_INDEX]]

    with open(WORDLIST, 'r') as _file:
        words = [_.replace("\n", "") for _ in _file.readlines()]

    with Pool(CONCURRENCY) as pool:
        for url in urls:
            TIMESTAMP = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            protocol, domain, port = get_url_parts(url)
            utils.make_domain_dir_structure(domain)
            directory = utils.get_directory_path(domain)
            output_file = f'{directory}/content-discovery_{protocol}-{domain}-{port}_{os.path.basename(WORDLIST)}_{TIMESTAMP}.txt'
            payload = prepare_payload(url, words)
            result = pool.apply_async(
                enumerate_content, args=(payload, output_file))
            results.append(result)
        [result.wait() for result in results]
