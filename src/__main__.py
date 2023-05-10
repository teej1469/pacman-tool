import os, subprocess, argparse
from sys import argv
from __pacman_tool__ import *
import argparse
import sudo, argparse


def package_list(packages: list) -> list:       # Update: I fixed that shit!
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
            ignore = inp(message.IGNORE_PROMPT)
            if ignore == "":    # Handling no input - assuming no corrections.
                approved = True
                break
            ignore = ignore.strip().split(" ")
            for i in ignore:            # Forcing i to be an int (also preventing
                if "q" or "exit" in i.lower():
                    print(message.EMPTY_EXIT)
                    return(None)
                    break

                i = int(i)                        # bad inputs from the user)
                try:
                    pkgs[i] = None         # Removes specified packages from pkgs list.
                except TypeError():
                    pkgs.clear()
            if None in pkgs:
                n = True
                while n:
                    try:
                        pkgs.remove(None)
                    except ValueError: 
                        n = False
                        pass

            if len(pkgs) == 0:          # Wrongfully returns true sometimes - investigate
                print(message.EMPTY_EXIT)
                return(None)
                break

            approved = input(message.MODIFY_CONFIRM(pkgs))
            if approved.lower() == "y":
                approved = True
            elif approved.lower() == "n":
                print(message.EMPTY_EXIT)
                return(None)
                break
            clear()

        return pkgs
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()


def arguments(app:dict) -> list: 
    try:
        argparse.HelpFormatter(prog=app.get("Name"))
        argParser = argparse.ArgumentParser(prog=app.get("ExecName"),description=f"{app.get('Name')} is a simple pacman tool written in python for bulk package operations.")
        
        argParser.add_argument("-v", "--version", action="version", version=f'%(prog)s {app.get("Stage")} {app.get("Version")}')
        action = argParser.add_mutually_exclusive_group()
        action.required = True
        action.add_argument("-R", type=str, help="Purge Pacman packages filtered by name", metavar="pkg")
        action.add_argument("-L", type=str, help="Resyncronize packages filtered by name", metavar="pkg")
        argParser.conflict_handler
        args = argParser.parse_args()

        action = None
        for i in args._get_kwargs():
            if not None in i:
                action = str(i)[2:3]
                fltr = str(i).lower()[7:-2]
                return [action, fltr]
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()

def packages(pkg_filter:str) -> list: 
    try:
        if pkg_filter.strip() == "":
            pkgs = subprocess.check_output(f"pacman -Q|cut -f 1 -d \" \"", shell=True).decode().split("\n")
        pkgs = subprocess.check_output(f"pacman -Q|cut -f 1 -d \" \" | grep {pkg_filter}", shell=True).decode().split("\n")
        pkgs:list = list(filter(None, pkgs))
        pkgs.sort()
        return pkgs
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()

def main():
    try:
        args = arguments(app=info.app)
        pkgs = packages(args[1])

        if args[0] == "R":
            remove(package_list(pkgs))
        elif args[0] == "L":
            sync(package_list(pkgs))
        elif args[0] == "":
            raise(NotImplementedError("Package syncing is not yet supported."))
    except KeyboardInterrupt:
        print(message.KEYBOARD_INTERRUPT)
        exit()
main() # runs the script.
