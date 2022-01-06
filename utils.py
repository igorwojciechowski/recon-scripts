from typing import Optional
import psutil
import time
import os
from pathlib import Path


def wait_for_process(pid: int) -> None:
    """
    Waits until a process with a given pid is either completed or in zombie status
    @param pid (int)  process pid
    """
    while pid in psutil.pids() and psutil.Process(pid).status() != psutil.STATUS_ZOMBIE:
        time.sleep(0.5)


def make_domain_dir_structure(domain: str) -> None:
    """
    Creates durectory structure for a given domain, e.g.: `com/test1/test2/test2.test1.com/`
    for `test2.test1.com` domain
    """
    subs = domain.split('.')
    subs.reverse()
    r = []
    for subdomain in subs:
        r.append(subdomain)
        if len(r) == 1:
            continue
        a = r.copy()
        a.reverse()
        path = Path(f"{'/'.join(r)}/{'.'.join(a)}")
        path.mkdir(parents=True)


def get_directory_path(directory: str) -> Optional(str):
    """
    Returns relative path of a found directory
    """
    for root, dirs, files in os.walk('.'):
        if directory in dirs:
            return f"{root}/{directory}"
