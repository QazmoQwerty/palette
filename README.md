# Palette

A command palette for your operating system

## Description

*Palette* holds a list of easy-access commands and when prompted displays a searchable cheat-sheet including the keyboard shortcut each command is bound to.

## Usage

*Palette* runs as a daemon (`paletted`), and is controlled through `palette` which communicates with the daemon through a socket.

The program is designed to also manage your keyboard shortcuts for you by creating its own instance of [sxhkd](https://github.com/baskerville/sxhkd) with a generated configuration.

## Configuring

*Palette* is configured through a JSON file, with each command containing a *"description"*, *"exec"* string, and an optional *keybinding*:

```
description: A string describing the command.
keybinding [OPTIONAL]: Keybinding for the command. Note that the syntax for this field is identical to sxhkd's keybinding syntax.
exec: The string to execute with `sh -c EXEC_STRING` whenever the command is run.
```

For an example configuration, see [here](examples/simple-example.json).

### Paletted

```
usage: paletted [-h] -c COMMANDS -b {none,sxhkd} [-v] [-V] [-s SOCKET]

Daemon process for palette

optional arguments:
  -h, --help            show this help message and exit
  -c COMMANDS, --commands COMMANDS
                        Commands json file path
  -b {none,sxhkd}, --backend {none,sxhkd}
                        Backend to use for keybindings management
  -v, --version         Show version number and exit
  -V, --verbose         Enable verbose output
  -s SOCKET, --socket SOCKET
                        Socket to listen for incoming connections
```

### Palette

```
usage: palette COMMAND

Controls the Palette daemon by communication with it through a socket.

commands:
    help   - Show this help message and exit.
    show   - Show the command palette.
    quit   - Ask paletted to suicide.
    reload - Reload the commands json file. 
             If a keybindings backend is running, 
             the keybindings will also be updated accordingly.
```

## Installation

Install from pypi:

```
sudo pip3 install commandpalette
```

Build and install from source:

```
git clone https://github.com/QazmoQwerty/palette
cd palette
make build
sudo make install
```