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

class CmdArguments(NamedTuple):
    commands_path: str
    keybindings_backend: str
    verbose: bool
    socket_path: str

def parse_arguments() -> CmdArguments:
    parser = ArgumentParser(description='Daemon process for palette')
    parser.add_argument(
        '-c', '--commands',
        type = str,
        required = True,
        help = 'Commands json file path'
    )
    parser.add_argument(
        '-b', '--backend',
        type = str,
        required = True,
        default = 'none',
        choices = ['none', 'sxhkd'],
        help = 'Backend to use for keybindings management'
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
        default = '/tmp/palette_socket',
        help = 'Socket to listen for incoming connections'
    )
    args = parser.parse_args()
    return CmdArguments(args.commands, args.backend, args.verbose, args.socket)

def get_keybindings_manager(args: CmdArguments) -> KeybindingsManager:
    if args.keybindings_backend == 'none':
        return KeybindingsManagerMock()
    if args.keybindings_backend == 'sxhkd':
        return Sxhkd('/tmp/palette_sxhkdrc')
    raise Exception('Unreachable')

def run():
    args = parse_arguments()
    configuration = Configuration()

    commands_manager = CommandsManager(args.commands_path)
    keybindings_manager = get_keybindings_manager(args)
    keybindings_manager.load(commands_manager.get_commands().values())
    with keybindings_manager:
        connection_handler = PaletteConnectionHandler(commands_manager, keybindings_manager, configuration)
        with UnixSocketServer(args.socket_path, connection_handler) as server:
            server.run()

def main() -> int:
    try:
        run()
    except QuitException:
        return 0
    return 1

if __name__ == '__main__':
    main()
