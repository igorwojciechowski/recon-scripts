#!/usr/bin/env python3
import subprocess
from datetime import datetime
from multiprocessing import Pool
import utils
import os
import argparse


resume_file = './websearch-resume.cfg'

def enumerate_content(url: str, wordlist: str, output_file: str) -> None:
    proc = subprocess.Popen(["websearch", "-u", url, "-w", wordlist],
                            stdin=subprocess.PIPE,
                            stderr=subprocess.DEVNULL,
                            stdout=open(output_file, 'a'))
    proc.wait()


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


def save(url: str, index: int):
    with open(resume_file, 'a') as _file:
        _file.writelines([url, index])


def load():
    with open(resume_file, 'r') as _file:
        return int(_file.readlines()[1])


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--urls', type=str, required=True)
    arg_parser.add_argument('-w', '--wordlist', type=str,
                            help="wordlist", required=True)
    arg_parser.add_argument('-c', '--concurrency', type=int,
                            default=5, help="Number of max parallel httpx processes")
    arg_parser.add_argument('-si', '--start_index',
                            type=int, default=0, help="Start index")
    arg_parser.add_argument('-ei', '--end_index', type=int)
    arg_parser.add_argument('--resume', action="store_true")
    args = arg_parser.parse_args()

    urls_file = args.urls
    wordlist = args.wordlist
    concurrency = args.concurrency

    urls = []
    results = []

    with open(urls_file, 'r') as _file:
        start_index = args.start_index
        end_index = args.end_index if args.end_index else len(
            _file.readlines())
        if args.resume:
            start_index = load()
        urls = [_.replace("\n", "")
                for _ in _file.readlines()[start_index:end_index]]

    with Pool(concurrency) as pool:
        for index, url in enumerate(urls):
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            protocol, domain, port = get_url_parts(url)
            utils.make_domain_dir_structure(domain)
            directory = utils.get_directory_path(domain)
            output_file = f'{directory}/content-discovery_{protocol}-{domain}-{port}_{os.path.basename(wordlist)}_{timestamp}.txt'
            result = pool.apply_async(
                enumerate_content, args=(url, wordlist, output_file))
            results.append(result)
            save(url, index)
        [result.wait() for result in results]
