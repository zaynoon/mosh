#!/bin/sh
LD_PRELOAD=/home/cgull/src/wsl-forkpty-shim/forkpty.so strace -qqTttffo mosh.strace /home/cgull/src/mosh-keithw/scripts/mosh --client=/home/cgull/src/mosh-keithw/src/frontend/mosh-client --server=/home/cgull/src/mosh-keithw/src/frontend/mosh-server --local 127.0.0.1

