import os, subprocess, argparse
from sys import argv
def clear():
    subprocess.run('clear')

def package_list(packages: list) -> list:
    try: 
        pkgs = packages
        list_pkgs: list = []    # List of packages exclusively for printing, not for using within code
        for i in pkgs:
            list_pkgs.insert(0,f"{pkgs.index(i)}:\t\b\b{i}")
        if None in list_pkgs:
            list_pkgs.remove(None)
        
        approved = False        # Getting user's approval for packages to modify
        while approved != True:
            clear()
            print("\n".join(list_pkgs))
            ignore = input(f"What packages should be ignored? [E.g: '1 2 3 5']\n> ")
            if ignore == "":    # Handling no input - assuming no corrections.
                print(ignore)
                approved = True
                break
            ignore = ignore.strip().split(" ")
            for i in ignore:            # Forcing i to be an int (also preventing
                i = str(i)                        # bad inputs from the user)
                try:
                    pkgs.pop(str(i))         # Removes specified packages from pkgs list.
                except IndexError:
                    pkgs.clear()
    
            if len(pkgs) == 0:
                print("Nothing to do.")
                return(None)

            approved = input(f"Packages to modify:\n{', '.join(pkgs)}\nAre you sure you want to modify these packages? [y/N]\n> ")
            if approved.lower() == "y":
                approved = True
            clear()

        return pkgs
    except KeyboardInterrupt:
        print("Process killed by user.")
        exit()

def sync(packages: list):
    if not packages == None:
        for i in packages:
                    print(f"Syncing package: {i}")
                    subprocess.run(f"sudo pacman -Sy {i} --noconfirm --noprogressbar", shell=True, stdout=subprocess.DEVNULL)


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-v", "--version", action="version", version='%(prog)s alph0.2')
    action = argParser.add_mutually_exclusive_group()
    action.required = True
    action.add_argument("-R", type=str, help="Purge Pacman packages filtered by name", metavar="pkg")
    action.add_argument("-S", type=str, help="Resyncronize packages filtered by name", metavar="pkg")
    argParser.conflict_handler
    args = argParser.parse_args()
    # print(args._get_kwargs())           # For debugging

    action = ""
    for i in args._get_kwargs():
        if not None in i:
            action = str(i)[2:3]
            fltr = str(i)[7:-2]
    
    pkgs = subprocess.check_output(f"pacman -Q|cut -f 1 -d \" \" | grep {fltr}", shell=True).decode().split("\n")
    pkgs:list = list(filter(None, pkgs))
    pkgs.sort()

    print(action[2:3])
    if action == "R":
        for i in pkgs:
            subprocess.run(f"sudo pacman -Rdd {i} --noconfirm --noprogressbar", shell=True, stdout=subprocess.DEVNULL)
    elif action == "S":
        sync(package_list(pkgs))
main()
