from socket import socket
from typing import NamedTuple
from argparse import ArgumentParser

from libpalette.sxhkd import Sxhkd
from libpalette.version import VERSION
from libpalette.server import UnixSocketServer
from libpalette.exceptions import QuitException
from libpalette.configuration import Configuration
from libpalette.commands_manager import CommandsManager
from libpalette.connection_handler import ConnectionHandler
from libpalette.keybindings_manager import KeybindingsManager
from libpalette.connection_handler import PaletteConnectionHandler
from libpalette.keybindings_manager_mock import KeybindingsManagerMock

def parse_arguments() -> Configuration:
    DEFAULT_CONFIGURATION = Configuration('')

    parser = ArgumentParser(description='Daemon process for palette')
    parser.add_argument(
        '-c', '--commands',
        type = str,
        required = True,
        help = 'Commands json file path.'
    )
    parser.add_argument(
        '-b', '--backend',
        type = str,
        required = True,
        default = DEFAULT_CONFIGURATION.keybindings_backend,
        choices = ['none', 'sxhkd'],
        help = f'Backend to use for keybindings management (default is {DEFAULT_CONFIGURATION.keybindings_backend})'
    )
    parser.add_argument(
        '-v', '--version',
        action = 'version',
        version = VERSION,
        help = 'Show version number and exit'
    )
    parser.add_argument(
        '-V', '--verbose',
        action = 'store_true',
        help = 'Enable verbose output'
    )
    parser.add_argument(
        '-s', '--socket',
        type = str,
        default = DEFAULT_CONFIGURATION.socket_path,
        help = f'Socket to listen for incoming connections (default is {DEFAULT_CONFIGURATION.socket_path})'
    )
    args = parser.parse_args()
    return Configuration(
        commands_path = args.commands,
        keybindings_backend = args.backend,
        verbose = args.verbose,
        socket_path = args.socket
    )

def get_keybindings_manager(keybindings_backend: str) -> KeybindingsManager:
    if keybindings_backend == 'none':
        return KeybindingsManagerMock()
    if keybindings_backend == 'sxhkd':
        return Sxhkd('/tmp/palette_sxhkdrc')
    raise Exception('Unreachable')

def run():
    configuration = parse_arguments()

    commands_manager = CommandsManager(configuration.commands_path)
    keybindings_manager = get_keybindings_manager(configuration.keybindings_backend)
    keybindings_manager.load(commands_manager.get_commands().values())
    with keybindings_manager:
        connection_handler = PaletteConnectionHandler(commands_manager, keybindings_manager, configuration)
        with UnixSocketServer(configuration.socket_path, connection_handler) as server:
            server.run()

def main() -> int:
    try:
        run()
    except QuitException:
        return 0
    return 1

if __name__ == '__main__':
    main()
