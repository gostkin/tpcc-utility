#!/usr/bin/env python3

import os
import sys
import subprocess


# stupid and simple way to parse args, only for mvp, TODO: replace with argparse
cmake_arg = False
task_arg = ""

if len(sys.argv) > 3 or len(sys.argv) < 2:
    raise RuntimeError("You should provide task name")

for arg in sys.argv[1:]:
    if arg == "--cmake":
        cmake_arg = True
    else:
        task_arg = arg

if len(task_arg) == 0:
    raise RuntimeError("You should provide task name")

ACTIVE_DIR = "/".join(os.path.abspath(__file__).split('/')[:-1])
ACTIVE_TASK_DIR = os.path.join(ACTIVE_DIR, "task")

os.chdir(ACTIVE_DIR)

if os.path.exists("task"):
    rm_process = subprocess.check_call(["rm -rf %s" % ACTIVE_TASK_DIR], shell=True)

ln_dir = os.path.join(ACTIVE_DIR, "..",  task_arg)

print("moving to " + ln_dir)

ln_process = subprocess.check_call(["ln -s %s %s" % (ln_dir, ACTIVE_TASK_DIR)], shell=True)

if cmake_arg:
    build_dirs = ["build", "cmake-build-debug", "cmake-build-release"]

    PROJECT_ROOT_DIR = os.path.join(ACTIVE_DIR, "..", "..")
    for build_dir in build_dirs:
        build_dir_path = os.path.join(PROJECT_ROOT_DIR, build_dir)
        if os.path.exists(build_dir_path):
            os.chdir(build_dir_path)
            cmake_process = subprocess.check_call(["cmake .."], shell=True)
            os.chdir(ACTIVE_DIR)
