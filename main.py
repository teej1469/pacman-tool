import os, subprocess, argparse
def clear():
    subprocess.run('clear')

def package_list(pkgs: list) -> list:
    try: 
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
            if ignore.strip() == "":    # Handling no input - assuming no corrections.
                approved = True
                break
            ignore = ignore.split(" ")
            for i in ignore:            # Forcing i to be an int (also preventing
                i = int(i)              # bad inputs from the user)
                try:
                    pkgs.pop(i)         # Removes specified packages from pkgs list.
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

def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-v", "--version", action="version", version='%(prog)s alph0.1')
    purge = argParser.add_mutually_exclusive_group()
    purge.add_argument("-R", type=str, help="Purge Pacman packages filtered by name", metavar="pkg")
    args = argParser.parse_args()
    print(args.purge)
    
    to_purge = input("Filter?\n> ")    # Packages to be removed.

    pkgs = subprocess.check_output(f"pacman -Q|cut -f 1 -d \" \" | grep {to_purge}", shell=True).decode().split("\n")
    pkgs:list = list(filter(None, pkgs))
    pkgs.sort()




main()
