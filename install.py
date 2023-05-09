from subprocess import run,DEVNULL,check_output, CalledProcessError, PIPE, Popen
from os import mkdir,listdir,system,path
deps_present = False

def import_required():
    try:
        import sudo
        import argparse
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
    except ModuleNotFoundError as e:
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

import_required
python_bin = ["/bin/python3","/usr/bin/python3","/bin/python","/usr/bin/python"]
def bin(bins:list):
    task("Finding python binary")
    def exists(path:str):
        try: open(path,"r")
        except FileNotFoundError:
            return(False)
        else: return(True)

    def check_ver(path:str) -> list:
        if exists(path):
            ver = int(check_output(f"{path} --version", shell=True)
            .decode()
            .removeprefix("Python")[:-2]
            .replace(".", "")
            .strip())
            if ver >= 310:
                return [f"{path}",ver]

    def biggest(args: list):
        biggest = 0
        for i in args:
            if i >= biggest:
                biggest = i
        return biggest

    bin: list = []
    ver: list = []
    for i in python_bin:
        ver.append(check_ver(i)[1])
        bin.append(check_ver(i)[0])
    verindex = ver.index(biggest(ver))
    ok(f"Found python binary: {bin[verindex]}")
    return bin[verindex]


binary = bin(python_bin)
lib_dir = "/usr/lib/pacman-tool"
here = __file__

if deps_present == False:
    print("Installing required packages...")
    run(f"{binary} -m pip install -r ./requirements", shell=True, stdout=DEVNULL, stderr=DEVNULL)
    print("Installed required packages.")

    import sudo
    from colorama import Fore, Back, Style
    WARN = Fore.YELLOW
    ERR = Fore.RED
    OK = Fore.GREEN
    ACTION = Fore.BLACK
    IN = Fore.LIGHTCYAN_EX
    RESET = Fore.RESET
    SUDO = Fore.MAGENTA

    def warn(values: object):
        print(f"{WARN}[WARN] {values}{RESET}")
    def err(values: object):
        print(f"{ERR}[ERR!] {values}{RESET}")
    def ok(values: object):
        print(f"{OK}[ OK ] {values}{RESET}")
    def task(values: object):
        print(f"{ACTION}[TASK] {values}{RESET}")
    def style(values: object, style: object):
        print(f"{style}{values}{RESET}")
    def inp(values: object) -> str:
        return(input(f"{IN}[ IN ] {values}\n> {RESET}"))
    sudo_prompt = f"{SUDO}[SUDO] Sudo password required.\n> {RESET}"


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