% PALETTE(1) Palette 0.3.0
% Shalev Don Meiri
% February 4, 2022

# NAME

palette - A command palette for your operating system

# SYNOPSIS

paletted [ -h | -v | -V | -c COMMANDS | -b {none,sxhkd} | -s SOCKET ]

palette COMMAND [*OPTIONS*]

# DESCRIPTION

*Palette* holds a list of easy-access commands and when prompted displays a searchable cheat-sheet including the keyboard shortcut each command is bound to. It is designed to also manage your keyboard shortcuts for you by creating its own instance of [sxhkd](https://github.com/baskerville/sxhkd) with a generated configuration.

The program runs as a daemon (`paletted`), and is controlled through `palette` which communicates with the daemon through a socket.

# USAGE

## PALETTED

Palette runs as a daemon (`paletted`), and is controlled through `palette` which communicates with the daemon through a socket.

-h, \--help
:   Show help message and exit.

-v, \--version
:   Show version and exit.

-V, \--verbose
:   Enable verbose output.

-c, \--commands
:   Path to the json file which contains all the commands - this field is mandatory.

-s, \--socket
:   Socket to listen for incoming connections.

-b, \--backend
:   Backend to use for keybindings management.
    Options are {`sxhkd`, `none`}, default is `none`.

## PALETTE

`palette` controls the `paletted` daemon by communication with it through a socket.

show
:    Show the command palette.

quit
:   Ask `paletted` to suicide.

reload
:   Reload the commands json file. If a keybindings backend is running, the keybindings will also be updated accordingly.

## CONFIGURING

*Palette* is configured through a JSON file, with each command containing a *"description"*, *"exec"* string, and an optional *keybinding*:

```
description: A string describing the command.
keybinding [OPTIONAL]: Keybinding for the command. Note that the syntax for this field is identical to sxhkd's keybinding syntax.
exec: The string to execute with `sh -c EXEC_STRING` whenever the command is run.
```

# SEE ALSO

Source code can be found here: 
<https://github.com/QazmoQwerty/palette>
