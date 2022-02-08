import os
from argparse import ArgumentParser
from typing import NamedTuple, Optional

from strictyaml import YAML
from libpalette.logger import Logger

from libpalette.rofi import Rofi
from libpalette.sxhkd import Sxhkd
from libpalette.version import VERSION
from libpalette.server import UnixSocketServer
from libpalette.exceptions import QuitException
from libpalette.commands_manager import CommandsManager
from libpalette.keybindings_manager import KeybindingsManager
from libpalette.connection_handler import PaletteConnectionHandler
from libpalette.keybindings_manager_mock import KeybindingsManagerMock
from libpalette.configuration import ConfigurationFactory, set_configuration_singleton

class CmdArguments(NamedTuple):
    config_path: Optional[str]
    keybindings_backend: str
    socket_path: str
    verbose: bool
    validate_config: bool

def get_default_config_path() -> str:
    home = os.getenv("HOME")
    assert home is not None
    return f'{home}/.config/palette/palette.yml'

def parse_arguments() -> CmdArguments:
    parser = ArgumentParser(description='Daemon process for palette')
    parser.add_argument(
        '-c', '--config',
        type = str,
        help = 'Config YAML file path (defaults to "$HOME/.config/palette/palette.yml").'
    )
    parser.add_argument(
        '-b', '--backend',
        type = str,
        default = 'sxhkd',
        choices = ['none', 'sxhkd'],
        help = f'Backend to use for keybindings management (defaults to "sxhkd")'
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
        '--validate',
        action= 'store_true',
        help = 'Validate configuration file and exit'
    )
    parser.add_argument(
        '-s', '--socket',
        type = str,
        default = '/tmp/palette_socket',
        help = f'Socket to listen for incoming connections'
    )
    args = parser.parse_args()
    return CmdArguments(
        config_path = args.config,
        keybindings_backend = args.backend,
        socket_path = args.socket,
        verbose = args.verbose,
        validate_config = args.validate
    )

def get_keybindings_manager(keybindings_backend: str) -> KeybindingsManager:
    if keybindings_backend == 'none':
        return KeybindingsManagerMock()
    if keybindings_backend == 'sxhkd':
        return Sxhkd('/tmp/palette_sxhkdrc')
    raise Exception('Unreachable')

def run():
    cmd_arguments = parse_arguments()
    logger = Logger(cmd_arguments.verbose)

    configuration_factory = ConfigurationFactory(cmd_arguments.config_path or get_default_config_path())
    set_configuration_singleton(configuration_factory.create())

    if cmd_arguments.validate_config:
        print('Configuration is valid.')
        raise QuitException

    rofi = Rofi(cmd_arguments.socket_path)
    commands_manager = CommandsManager()
    keybindings_manager = get_keybindings_manager(cmd_arguments.keybindings_backend)
    keybindings_manager.load(commands_manager.get_commands().values())
    with keybindings_manager:
        connection_handler = PaletteConnectionHandler(logger, commands_manager, keybindings_manager, configuration_factory, rofi)
        with UnixSocketServer(cmd_arguments.socket_path, connection_handler) as server:
            server.run()

def main() -> int:
    try:
        run()
    except QuitException:
        return 0
    return 1

if __name__ == '__main__':
    main()
