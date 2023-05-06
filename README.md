# pacman-tool

Simple python tool I'm working on that essentially acts as a bulk Pacman package manipulation tool.
I wrote this cuz I got tired of manually searching and deleting all packages related to PipeWire for
reinstallation.

# TODO
* [ ] Full system update/upgrade on dry run (Like with `yay`)
* [ ] Continue migrating all text in `__main.py__` to `__pacman_tool__.message`
* [ ] Create install script that installs `__main__.py` and `__pacman_tool__.py` to `/usr/lib/pacman_tool` so that the script can be run in any directory without returning `/bin/python: can't open file '/CURRENT_DIRECTORY/src/__main__.py': [Errno 2] No such file or directory` 
* [ ] (Maybe) AUR support
* [ ] (Maybe) Complete rewrite in Rust :)
