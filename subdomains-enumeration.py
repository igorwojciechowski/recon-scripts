#!/usr/bin/env python3
import sys
import multiprocessing
from multiprocessing import Manager
import subprocess
from datetime import datetime

from utils import wait_for_process


def stage_1(shared_dict: dict, domain: str, output: str) -> None:
    """
    Run amass enumeration
    """
    proc = subprocess.Popen(
        ['amass', 'enum', '-brute', '-d', domain, '-nolocaldb'], stdout=open(output, 'w'))
    shared_dict['stage_1'] = proc.pid


def stage_2(shared_dict: dict, domain: str, output: str) -> None:
    """
    Run waybackurls
    """
    proc = subprocess.Popen(['waybackurls', domain], stdout=open(output, 'w'))
    shared_dict['stage_2'] = proc.pid


def stage_3(shared_dict: dict, domain: str, input: str, output: str):
    """
    Grep subdomains from waybackurls
    Needs stage 2
    """
    proc = subprocess.Popen(
        ["grep", "-oP", f"([a-zA-Z0-9-_]+[.])*{domain}"],
        stdin=open(input, 'r'),
        stdout=open(output, 'a')
    )
    shared_dict['stage_3'] = proc.pid


def stage_4(input_files: list, output: str):
    """
    Merge domains lists
    Needs: stage 1 and stage 3
    """
    domains = set()
    for f in input_files:
        with open(f, 'r') as file:
            for line in file.readlines():
                domains.add(line.replace('\n', ''))
    with open(output, 'w') as file:
        file.write('\n'.join(domains))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("No domain provided")
        sys.exit(1)

    DOMAIN = sys.argv[1]
    MANAGER = Manager()
    SHARED_DICT = MANAGER.dict()

    started = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    amass_output = f"amass-{DOMAIN}-{started}.txt"
    waybackurls_output = f"waybackurls-{DOMAIN}-{started}.txt"
    grepped_subdomains_output = f"waybackurls-domains-{DOMAIN}-{started}.txt"
    domains_output = f"subdomains-{DOMAIN}-{started}.txt"

    stage_1_job = multiprocessing.Process(
        target=stage_1, args=(SHARED_DICT, DOMAIN, amass_output))
    stage_2_job = multiprocessing.Process(
        target=stage_2, args=(SHARED_DICT, DOMAIN, waybackurls_output))
    stage_3_job = multiprocessing.Process(target=stage_3, args=(
        SHARED_DICT, DOMAIN, waybackurls_output, grepped_subdomains_output))
    stage_4_job = multiprocessing.Process(
        target=stage_4, args=([amass_output, grepped_subdomains_output], domains_output))

    stage_1_job.start()
    stage_1_job.join()
    stage_2_job.start()
    stage_2_job.join()
    wait_for_process(SHARED_DICT['stage_2'])
    stage_3_job.start()
    stage_3_job.join()
    wait_for_process(SHARED_DICT['stage_1'])
    wait_for_process(SHARED_DICT['stage_3'])
    stage_4_job.start()
    stage_4_job.join()
