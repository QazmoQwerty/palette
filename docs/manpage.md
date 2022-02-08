% PALETTE(1) Palette 0.4.0
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

-c, \--config
:   Configuration YAML file path (defaults to "$HOME/.config/palette/palette.yml").

-s, \--socket
:   Socket to listen for incoming connections.

-b, \--backend
:   Backend to use for keybindings management.
    Options are {`sxhkd`, `none`}, default is `sxhkd`.

\--validate
:   Validate configuration file and exit

## PALETTE

`palette` controls the `paletted` daemon by communication with it through a socket.

help
:   Show help message and exit.

show
:   Show the command palette.

quit
:   Ask `paletted` to suicide.

reload
:   Reload the configuration YAML file. If a keybindings backend is running, the keybindings will also be updated accordingly.

## CONFIGURING

*Palette* is configured through a YAML file, with each command containing a *description*, *exec* string, an optional *keybinding*, and optional *meta* keywords:

```
description: A string describing the command.
exec: The string to execute with `sh -c EXEC_STRING` whenever the command is run.
keybinding [OPTIONAL]: Keybinding for the command. Note that the syntax for this field is identical to sxhkd's keybinding syntax.
meta [OPTIONAL]: Additional invisible search terms for the command.
```

# SEE ALSO

Source code can be found here: 
<https://github.com/QazmoQwerty/palette>
