from subprocess import run, DEVNULL
from colorama import Fore, Back, Style 

WARN = Fore.YELLOW
ERR = Fore.RED
OK = Fore.GREEN
ACTION = Fore.BLACK
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

class message():
    SUDO_PROMPT = f"{SUDO}[SUDO] As this script uses pacman, and makes changes to installed packages, root permissions are required. Please authenticate:\n> {RESET}"
    IGNORE_PROMPT:str = "What packages should be ignored? [E.g: '1 2 3 5']\n> "
    EMPTY_EXIT:str = "Nothing to do."
    KEYBOARD_INTERRUPT:str = "\nKilled by user.\n"
    def MODIFY_CONFIRM(arg:list) -> str:
        return(f"Packages to modify:\n{', '.join(arg)}\nAre you sure you want to modify these packages? [y/N]\n> ")

def empty_exit():
    err(message.EMPTY_EXIT)
    return None

def clear():
    run('clear')

def remove(packages: list):
    try:
        if not packages == None:
            for i in pkgs:
                run(f"sudo -p \"{message.SUDO_PROMPT}\" pacman -Rdd {i} --noconfirm --noprogressbar", shell=True, stdout=DEVNULL)
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()

def sync(packages: list):
    try:
        if not packages == None:
            for i in packages:
                print(f"Syncing package: {i}")
                run(f"sudo -p \"{message.SUDO_PROMPT}\" pacman -Sy {i} --noconfirm --noprogressbar", shell=True, stdout=DEVNULL)
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()

class info():
    app = {
        "Stage": "Alpha",
        "Version": "0.0.7",
        "Name": "Pacman Tool",
        "ExecName": "pacman-tool",
        "Description": "is a simple tool written in Python for bulk Pacman package operation.",
        "Github": "https://github.com/teej1469/pacman-tool"
        }
    help = {
        "R": "Remove packages in bulk.", 
        "L": "Resync local packages in bulk.",
        "S": "Sync a singular package."
        }
