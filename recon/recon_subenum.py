#!/usr/bin/env python3
import argparse
from os import path
import multiprocessing
from multiprocessing import Manager
import subprocess
from datetime import datetime
import concurrent.futures

from recon.utils.utils import wait_for_process


STAGE_1 = 'stage_1'
STAGE_2 = 'stage_2'
STAGE_3 = 'stage_3'
RESULTS = 'results'


def run_amass(shared_dict: dict, domain: str, output: str) -> None:
    proc = subprocess.Popen(
        ['amass', 'enum', '-brute', '-d', domain, '-nolocaldb'], stdout=open(output, 'w'))
    shared_dict[STAGE_1] = proc.pid


def run_waybackurls(shared_dict: dict, domain: str, output: str) -> None:
    proc = subprocess.Popen(['waybackurls', domain], stdout=open(output, 'w'))
    shared_dict[STAGE_2] = proc.pid


def grep_domains(shared_dict: dict, domain: str, input: str, output: str):
    proc = subprocess.Popen(
        ["grep", "-oP", f"([a-zA-Z0-9-_]+[.])*{domain}"],
        stdin=open(input, 'r'),
        stdout=open(output, 'a')
    )
    shared_dict[STAGE_3] = proc.pid


def merge_domains_lists(shared_dict, input_files: list, output: str):
    domains = set()
    for f in input_files:
        with open(f, 'r') as file:
            for line in file.readlines():
                domains.add(line.replace('\n', ''))
    with open(output, 'w') as file:
        file.write('\n'.join(domains))
    shared_dict[RESULTS] = domains
    

def enumerate_subdomains(domain):
    manager = Manager()
    shared_dict = manager.dict()
    started = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    amass_output = f"amass-{domain}-{started}.txt"
    waybackurls_output = f"waybackurls-{domain}-{started}.txt"
    grepped_subdomains_output = f"waybackurls-domains-{domain}-{started}.txt"
    domains_output = f"subdomains-{domain}-{started}.txt"

    stage_1_job = multiprocessing.Process(
        target=run_amass, args=(shared_dict, domain, amass_output))
    stage_2_job = multiprocessing.Process(
        target=run_waybackurls, args=(shared_dict, domain, waybackurls_output))
    stage_3_job = multiprocessing.Process(target=grep_domains, args=(
        shared_dict, domain, waybackurls_output, grepped_subdomains_output))
    stage_4_job = multiprocessing.Process(
        target=merge_domains_lists, args=(shared_dict, [amass_output, grepped_subdomains_output], domains_output))

    stage_1_job.start()
    stage_1_job.join()
    stage_2_job.start()
    stage_2_job.join()
    wait_for_process(shared_dict[STAGE_2])
    stage_3_job.start()
    stage_3_job.join()
    wait_for_process(shared_dict[STAGE_1])
    wait_for_process(shared_dict[STAGE_3])
    stage_4_job.start()
    stage_4_job.join()
    return shared_dict[RESULTS]


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--domains', help="Single domain or path to file", type=str, required=True)
    arg_parser.add_argument('-t', '--threads', help="Number of concurrent threads", type=int, default=5)
    arg_parser.add_argument('-o', '--output', help="Output file", type=str)
    args = arg_parser.parse_args()

    subdomains = []
    started = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    threads = args.threads
    output = args.output if args.output else f"subdomains-{started}.txt"
    domains = [args.domains]

    if path.exists(args.domains):
        domains = []
        with open(args.domains, 'r') as domains_file:
            domains = [domain.strip() for domain in domains_file.readlines()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(enumerate_subdomains, domains)
        for result in results:
            [subdomains.append(_) for _ in result]

    with open(output, 'w') as file:
        file.write('\n'.join(subdomains))


if __name__ == '__main__':
    main()
    