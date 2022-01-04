#!/bin/bash
# ---
# nohup wrapper for spawning detached processes (with no nohup.out output)
# ---
nohup "$@" </dev/null >/dev/null 2>&1 &