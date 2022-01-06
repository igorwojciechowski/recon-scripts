#!/usr/bin/env python3
# Process Management script
import psutil
import sys
import os
import time

BINARIES = [
    "python3",
    "amass",
    "httpx",
    "waybackurls"
]

COMMANDS = [
    "show"
]

if len(sys.argv) < 2:
    sys.exit("no command provided")

if sys.argv[1] not in COMMANDS:
    nl = "\n\t"
    sys.exit(f"wrong command.\n\navailable commands:\n\t{nl.join(COMMANDS)}")

COMMAND = sys.argv[1]
OPTIONS = [option for option in sys.argv[2:]]

def show():
    """
    Displays running processes in 5 seconds intervals.
    """
    while True:
        try:
            os.system("clear")
            sys.stdout.flush()
            print(f"\033[1;32;40mCurrently running processes: {len([p for p in psutil.process_iter() if p.name() in BINARIES])}\n")
            for binary in BINARIES:
                processes = [process for process in psutil.process_iter() if process.name() == binary]
                if processes:
                    print(f"\033[1;36;40m {binary}")
                for process in processes:
                    print(f"\033[0;32;40m\t{process.pid:5}\t{' '.join(process.cmdline()):50}")
            time.sleep(5)
        except KeyboardInterrupt:
            sys.exit()

if COMMAND == "show":
    show()

