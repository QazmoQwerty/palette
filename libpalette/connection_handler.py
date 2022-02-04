import datetime
import subprocess
from typing import Callable, List

from libpalette.rofi import Rofi
from libpalette.command import CommandId
from libpalette.connection import Connection
from libpalette.configuration import Configuration
from libpalette.commands_manager import CommandsManager
from libpalette.keybindings_manager import KeybindingsManager
from libpalette.exceptions import PaletteError, QuitException, CommandNotFoundError

class ConnectionHandler:
    def handle_connection(self, connection: Connection) -> None:
        raise NotImplementedError

HELP_MESSAGE = """\
usage: palette COMMAND

Controls the Palette daemon by communication with it through a socket.

commands:
    help   - Show this help message and exit.
    show   - Show the command palette.
    quit   - Ask paletted to suicide.
    reload - Reload the commands json file. 
             If a keybindings backend is running, 
             the keybindings will also be updated accordingly.
"""

class PaletteConnectionHandler(ConnectionHandler):
    _commands_manager: CommandsManager
    _keybindings_manager: KeybindingsManager
    _rofi: Rofi

    def __init__(self, commands_manager: CommandsManager, keybindings_manager: KeybindingsManager, configuration: Configuration) -> None:
        self._commands_manager = commands_manager
        self._keybindings_manager = keybindings_manager
        self._rofi = Rofi(configuration)
    
    def _handle_no_arguments(self, args: List[str], connection: Connection) -> None:
        connection.send_error('No arguments given')
    
    def _handle_unknown_command(self, args: List[str], connection: Connection) -> None:
        connection.send_error(f'Unknown command {repr(args[0])}')
    
    def _execute_command(self, identifier: CommandId) -> None:
        command = self._commands_manager.get_command(identifier)
        if command is None:
            raise CommandNotFoundError(identifier)
        command.last_used = datetime.datetime.now()
        subprocess.Popen(['sh', '-c', command.exec_string])
    
    def _handle_show(self, args: List[str], connection: Connection) -> None:
        identifier = self._rofi.show_palette(self._commands_manager.get_commands())
        if identifier is not None:
            self._execute_command(identifier)
    
    def _handle_help(self, args: List[str], connection: Connection) -> None:
        if len(args) == 1:
            connection.send(HELP_MESSAGE)
        else:
            connection.send_error('Invalid arguments (expected 0)')

    def _handle_reload(self, args: List[str], connection: Connection) -> None:
        self._commands_manager.reload()
        self._keybindings_manager.load(self._commands_manager.get_commands().values())
    
    def _handle_quit(self, args: List[str], connection: Connection) -> None:
        raise QuitException

    def _get_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_no_arguments if len(args) == 0 else {
            'show': self._handle_show,
            'help': self._handle_help,
            'quit': self._handle_quit,
            'reload': self._handle_reload,
        }.get(args[0]) or self._handle_unknown_command
    
    def handle_connection(self, connection: Connection) -> None:
        args = connection.recv_args()
        print('Args:', args)
        try:
            self._get_handler(args)(args, connection)
        except PaletteError as e:
            connection.send_error(str(e))
