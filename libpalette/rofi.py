import os
import subprocess
from typing import Iterable, Optional, Dict, List

from libpalette.utils import remove_whitespace
from libpalette.configuration import get_configuration
from libpalette.command import Command, CommandId, COMMAND_ID_SIZE

class Rofi:
    _socket_path: str

    def __init__(self, socket_path: str) -> None:
        self._socket_path = socket_path

    def show_palette(self, commands: Dict[CommandId, Command]) -> None:
        with open(get_configuration()['rofi']['mode_script']['input_path'].data, 'wb') as file:
            file.write(self._get_rofi_input(commands))
        
        env_copy = os.environ.copy()
        env_copy['PALETTE_SOCKET'] = self._socket_path
        env_copy['PALETTE_ROFI_INPUT_PATH'] = get_configuration()['rofi']['mode_script']['input_path'].data

        arguments = ['rofi', '-modi', f'palette:palette-rofi-script', '-show', 'palette']
        if get_configuration()['rofi']['additional_arguments'].data is not None:
            arguments += get_configuration()['rofi']['additional_arguments'].data
        
        print(repr(arguments))

        subprocess.Popen(arguments, env=env_copy)
    
    def _opposite_align(self, left: str, right: str, length: int) -> str:
        return left + ' ' * (length - len(right) - len(left)) + right
    
    def _format_keybinding(self, keybinding: str) -> str:
        if not get_configuration()['rofi']['modifier_icons']['is_active'].data:
            return f'[{keybinding}]'
        
        return ';'.join(
            '+'.join(
                key.replace('alt', get_configuration()['rofi']['modifier_icons']['alt'].data)
                   .replace('ctrl', get_configuration()['rofi']['modifier_icons']['ctrl'].data)
                   .replace('super', get_configuration()['rofi']['modifier_icons']['super'].data)
                   .replace('shift', get_configuration()['rofi']['modifier_icons']['shift'].data)
                for key in chord.split('+')
            ) for chord in remove_whitespace(keybinding).split(';')
        )
    
    def _command_rofi_description(self, command: Command) -> str:
        return (
            command.description if command.keybinding is None
            else self._opposite_align(
                left = command.description,
                right = self._format_keybinding(command.keybinding),
                length = get_configuration()['rofi']['window_width'].data
            ) if get_configuration()['rofi']['opposite_align_commands_and_shortcuts'].data
            else f'{command.description} {self._format_keybinding(command.keybinding)}'
        )
    
    def _command_rofi_input(self, command: Command) -> str:
        metadata = f'\x1fmeta\x1f{command.metadata}' if command.metadata else ''
        return f'{self._command_rofi_description(command)}\0info\x1f{command.identifier}' + metadata

    def _properly_sorted(self, commands: Iterable[Command]) -> List[Command]:
        """Sorts the commands first by their last used time, and then by lexical order"""
        sorting_key = lambda command: (-command.last_used.toordinal(), command.description.casefold())
        return sorted(commands, key=sorting_key)

    def _get_rofi_input(self, commands: Dict[CommandId, Command]) -> bytes:
        return '\n'.join([
            "\0no-custom\x1ftrue",
            *map(self._command_rofi_input, self._properly_sorted(commands.values()))
        ]).encode()
