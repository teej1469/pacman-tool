from subprocess import run, DEVNULL

class message():
    SUDO_PROMPT:str = "[Sudo] As this script uses pacman, and makes changes to installed packages, root permissions are required. Please authenticate:\n> "
    IGNORE_PROMPT:str = "What packages should be ignored? [E.g: '1 2 3 5']\n> "
    EMPTY_EXIT:str = "Nothing to do."
    KEYBOARD_INTERRUPT:str = "\nKilled by user.\n"
    def MODIFY_CONFIRM(arg:list) -> str:
        return(f"Packages to modify:\n{', '.join(arg)}\nAre you sure you want to modify these packages? [y/N]\n> ")

def empty_exit():
    print(message.EMPTY_EXIT)
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