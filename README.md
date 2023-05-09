<h1 align="center">Pacman Tool</h1>
<p align="center">
  <img alt="Github code size in bytes" src="https://img.shields.io/github/languages/code-size/teej1469/pacman-tool?style=plastic">
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/teej1469/pacman-tool?style=plastic">
  <img alt="GitHub" src="https://img.shields.io/github/license/teej1469/pacman-tool?color=informational&style=plastic">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/teej1469/pacman-tool?style=plastic">
  <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2023?style=plastic">
  <img alt="Version" src="https://img.shields.io/badge/version-Alpha--0.0.5-important?style=plastic">
</p>

Simple python tool I'm working on that essentially acts as a bulk Pacman package manipulation tool.
I wrote this cuz I got tired of manually searching and deleting all packages related to PipeWire for
reinstallation.

*NOTE: THIS IS ONLY INTENDED FOR ARCH AND ARCH-BASED LINUX DISTRIBUTIONS THAT USE PACMAN AS THEIR PRIMARY PACKAGE MANAGER. DO NOT POST ISSUES IF IT DOES NOT WORK ON A NON-ARCH-BASED DISTRO, FIND A DIFFERENT TOOL.*

## Installation

1. Ensure you have Python 3.7 or later installed. Check with `python --version`. *(Newer is preferred.)*
2. Clone the repository:`git clone https://github.com/teej1469/pacman-tool`, `cd pacman-tool`
3. Run install.py (`python3 ./install.py`) script and follow the prompts.

## TODO

* [x] Create an installer
* [ ] Built-in update/uninstall.
* [ ] Full system update/upgrade on dry run (Like with`yay`)
* [ ] Continue migrating all text in`__main.py__` to`__pacman_tool__.message`
* [ ] (Maybe) AUR support
* [ ] (Maybe) Complete rewrite in Rust :)
