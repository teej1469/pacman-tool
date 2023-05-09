# pacman-tool

Simple python tool I'm working on that essentially acts as a bulk Pacman package manipulation tool.
I wrote this cuz I got tired of manually searching and deleting all packages related to PipeWire for
reinstallation.
*NOTE: THIS IS ONLY INTENDED FOR ARCH AND ARCH-BASED LINUX DISTRIBUTIONS THAT USE PACMAN AS THEIR PRIMARY PACKAGE MANAGER. DO NOT POST ISSUES IF IT DOES NOT WORK ON A NON-ARCH-BASED DISTRO, FIND A DIFFERENT TOOL.*

## Installation

1. Clone the repository:`git clone https://github.com/teej1469/pacman-tool`,`cd pacman-tool`
2. Run the install script:`/bin/python install.py`. It will install all the necessary modules, and copy the source files to`/usr/lib/pacman-tool`.
3. The tool is now installed, you can now use it as you wish. Be sure to update frequently though!

## TODO

* [ ] Full system update/upgrade on dry run (Like with`yay`)
* [ ] Continue migrating all text in`__main.py__` to`__pacman_tool__.message`
* [ ] Create install script that installs`__main__.py` and`__pacman_tool__.py` to`/usr/lib/pacman_tool` so that the script can be run in any directory without returning`/bin/python: can't open file '/CURRENT_DIRECTORY/src/__main__.py': [Errno 2] No such file or directory`
* [ ] (Maybe) AUR support
* [ ] (Maybe) Complete rewrite in Rust :)
