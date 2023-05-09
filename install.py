from subprocess import run,DEVNULL,check_output, CalledProcessError, PIPE, Popen
from os import mkdir,listdir,system,path,terminal_size
from sys import executable

deps_present = False
try:
    try:
        import sudo
        import argparse
        from colorama import Fore, Back, Style
    except ModuleNotFoundError:
        if deps_present == False:
            print("Installing required packages...")
            run(f"{executable} -m pip install -r ./requirements", shell=True, stdout=DEVNULL, stderr=DEVNULL)
            print("Installed required packages.")
    finally: 
        import sudo, argparse
        from colorama import Fore, Back, Style 

        WARN = Fore.YELLOW
        ERR = Fore.RED
        OK = Fore.GREEN
        ACTION = Fore.BLACK
        IN = Fore.LIGHTCYAN_EX
        RESET = Fore.RESET
        SUDO = Fore.MAGENTA 
        deps_present = True

        def warn(values: object):
            print(f"{WARN}[WARN] {values}{RESET}")
        def err(values: object):
            print(f"{ERR}[ERR ] {values}{RESET}")
        def ok(values: object):
            print(f"{OK}[ OK ] {values}{RESET}")
        def task(values: object):
            print(f"{ACTION}[TASK] {values}{RESET}")
        def style(values: object, style: object):
            print(f"{style}{values}{RESET}")
        def inp(values: object) -> str:
            return(input(f"{IN}[ IN ] {values}\n> {RESET}"))
        sudo_prompt = f"{SUDO}[SUDO] Sudo password required.\n> {RESET}"
        ok("Dependencies present")
except Exception:
    def warn(values: object):
        print(f"[WARN] {values}")
    def err(values: object):
        print(f"[ERR ] {values}")
    def ok(values: object):
        print(f"[ OK ] {values}")
    def task(values: object):
        print(f"[TASK] {values}")
    def inp(values: object) -> str:
        return(input(f"[ IN ] {values}\n> "))
    sudo_prompt = f"[SUDO] Root password required.\n> "
    warn("Coloured outputs unavailable.")

lib_dir = "/usr/lib/pacman-tool"
here = __file__

class Errors():
    class DirectoryNotEmptyError(OSError): ...
try:
    if not path.exists(lib_dir):
        warn(f"Need root permissions to create directory {lib_dir}")
        run(f"sudo -p '{sudo_prompt}' /bin/mkdir {lib_dir}",shell=True)
        ok(f"Created directory {lib_dir}")
    elif not path.isdir(lib_dir):
        raise NotADirectoryError(f"There exists a non-directory file in the place of {lib_dir}/")
    elif not len(listdir(lib_dir)) == 0:
        raise Errors.DirectoryNotEmptyError(f"There are already files inside {lib_dir}")
    else:
        warn(f"Directory {lib_dir}/ already exists, but is empty.")
except Errors.DirectoryNotEmptyError as or_:
    cont = inp("Empty directory and continue installation? [Y/n]").lower().strip()
    if cont == "y":
        run(f"sudo -p '{sudo_prompt}' rm -rf {lib_dir}/*", shell=True)
        ok("Removed unnecessary files")
except Exception as or_:
    err(or_)
    pass
    exit()

task("Writing runtime data to run script")

runscript = """#!/bin/bash
# Pacman Tool: A bulk package management tool written in Python.

/bin/python %s/__main__.py $@
""" % lib_dir

open("pacman_tool","w").write(runscript)

task("Moving files to %s" % lib_dir)
run(f"sudo -p '{sudo_prompt}' cp ./src/* {lib_dir}/", shell=True, stderr=DEVNULL)
run(f"sudo -p '{sudo_prompt}' cp ./pacman_tool {lib_dir}", shell=True)
ok("Files copied")
task("Creating symbolc link from %s/pacman_tool to /usr/bin/pacman_tool" % lib_dir)
run(f"sudo -p '{sudo_prompt}' ln -rs ./pacman_tool /usr/bin", shell=True)
ok("Installation complete! Run pacman_tool -h for info!")