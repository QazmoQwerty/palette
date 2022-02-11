# Palette

A command palette for your operating system.

![Demo](demo.gif)

## Description

*Palette* holds a list of easy-access commands and when prompted displays a searchable cheat-sheet including the keyboard shortcut each command is bound to.

## Usage

*Palette* runs as a daemon (`paletted`), and is controlled through `palette` which communicates with the daemon through a socket.

The program is designed to also manage your keyboard shortcuts for you by creating its own instance of [sxhkd](https://github.com/baskerville/sxhkd) with a generated configuration.

### Configuring

*Palette* is configured through a YAML file, with each command containing a *description*, *exec* string, an optional *keybinding*, and optional *meta* keywords:

```
description: A string describing the command.
exec: The string to execute with `sh -c EXEC_STRING` whenever the command is run.
keybinding [OPTIONAL]: Keybinding for the command. Note that the syntax for this field is identical to sxhkd's keybinding syntax.
meta [OPTIONAL]: Additional invisible search terms for the command.
```

For an example configuration, see [here](examples/simple-example.yml).

### Paletted

```
usage: paletted [-h] [-c CONFIG] [-b {none,sxhkd}] [-v] [-V] [--validate] [-s SOCKET]

Daemon process for palette

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config YAML file path (defaults to "$HOME/.config/palette/palette.yml").
  -b {none,sxhkd}, --backend {none,sxhkd}
                        Backend to use for keybindings management (defaults to "sxhkd")
  -v, --version         Show version number and exit
  -V, --verbose         Enable verbose output
  --validate            Validate configuration file and exit
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
    reload - Reload the configuration YAML file. 
             If a keybindings backend is running, 
             the keybindings will also be updated accordingly.
```

## Requirements

* rofi

* bspwm

* sxhkd

## Installation

Install from pypi:

```
sudo pip3 install commandpalette
```

Build and install from source:

```sh
git clone https://github.com/QazmoQwerty/palette
cd palette
sudo pip3 install -r requirements.txt
python3 -m build
sudo python3 -m pip install dist/commandpalette*.whl
```