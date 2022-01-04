import psutil
import time
import os

def wait_for_process(pid: int) -> None:
    """
    Waits until a process with a given pid is either completed or in zombie status
    @param pid (int)  process pid
    """
    while pid in psutil.pids() and psutil.Process(pid).status() != psutil.STATUS_ZOMBIE:
        time.sleep(0.5)

def mkdirs(path: str) -> None:
    directories = os.path.dirname(path)
    if not os.path.exists(directories):
        os.makedirs(directories)

def mkdir(directory: str) -> None:
    if not os.path.exists(directory):
        os.mkdir(directory)
