from subprocess import run,DEVNULL,check_output, CalledProcessError, PIPE, Popen
from os import mkdir,listdir,system,path,terminal_size
from sys import executable


dl_files = ["src/__main__.py", "src/__pacman_tool__.py", "install.py", "LICENSE", "README.md", "requirements"]
deps_present = False
already_exists = False
lib_dir = "/usr/lib/pacman-tool"
here = __file__
class Errors():
    class DirectoryNotEmptyError(OSError): ...
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
    if any(["__main__.py" in listdir(lib_dir), "__pacman_tool__.py"in listdir(lib_dir)]):
        warn("There is already a version of Pacman Tool installed.")
        if inp("Do you want to uninstall it? [Y/n]").lower().strip() == "y":
            run(f"sudo -p '{sudo_prompt}' rm -rf {lib_dir}/*", shell=True)
            run(f"sudo -p '{sudo_prompt}' rm -rf /usr/bin/pacman_tool", shell=True)
            ok("Successfully uninstalled.")
            if inp("Do you wish to continue installing?").lower().strip() == "y":
                pass
            else:
                err("Nothing to do.")
                exit()
        else:
            err("Nothing to do.")
            exit()
    else:
        warn(f"Files exist in {lib_dir}")
        if inp("Empty directory and continue installation? [Y/n]").lower().strip() == "y":
            run(f"sudo -p '{sudo_prompt}' rm -rf {lib_dir}/*", shell=True)
            ok("Removed obstructing files")
        else:
            err("Nothing to do.")
            exit()
except NotADirectoryError as or_:
    err(or_)
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
check_output(f"sudo -p '{sudo_prompt}' cp ./src/* {lib_dir}", shell=True, stderr=DEVNULL)
ok("Files copied")
task("Creating symbolc link from %s/pacman_tool to /usr/bin/pacman_tool" % lib_dir)
run(f"sudo -p '{sudo_prompt}' ln -rs ./pacman_tool /usr/bin", shell=True)

if inp(f"Remove unnecessary downloaded files? [Y/n]").lower().strip() == "y":
    for i in dl_files:
        run("rm ./%s -rf" % i, shell=True)
ok("Installation complete! Run pacman_tool -h for info!")