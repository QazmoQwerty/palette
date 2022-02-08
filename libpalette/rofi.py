import os
import subprocess
from typing import Iterable, Optional, Dict, List

from libpalette.utils import remove_whitespace
from libpalette.configuration import Configuration
from libpalette.command import Command, CommandId, COMMAND_ID_SIZE

class Rofi:
    _configuration: Configuration

    def __init__(self, configuration: Configuration) -> None:
        self._configuration = configuration
    
    def show_palette(self, commands: Dict[CommandId, Command]) -> None:
        with open(self._configuration.rofi_script_input_path, 'wb') as file:
            file.write(self._get_rofi_input(commands))
        env_copy = os.environ.copy()
        env_copy['PALETTE_SOCKET_PATH'] = self._configuration.socket_path
        env_copy['PALETTE_ROFI_INPUT_PATH'] = self._configuration.rofi_script_input_path
        subprocess.Popen(['rofi', '-modi', f'palette:palette-rofi-script', '-show', 'palette'], env=env_copy)
    
    def _opposite_align(self, left: str, right: str, length: int) -> str:
        return left + ' ' * (length - len(right) - len(left)) + right
    
    def _format_keybinding(self, keybinding: str) -> str:
        if not self._configuration.use_modifier_icons:
            return f'[{keybinding}]'
        
        return ';'.join(
            ''.join(
                key.replace('alt', self._configuration.alt_modifier_icon)
                   .replace('ctrl', self._configuration.ctrl_modifier_icon)
                   .replace('super', self._configuration.super_modifier_icon)
                   .replace('shift', self._configuration.shift_modifier_icon)
                for key in chord.split('+')
            ) for chord in remove_whitespace(keybinding).split(';')
        )
    
    def _command_rofi_description(self, command: Command) -> str:
        return (
            command.description if command.keybinding is None
            else self._opposite_align(
                left = command.description,
                right = self._format_keybinding(command.keybinding),
                length = self._configuration.rofi_window_width
            ) if self._configuration.opposite_align_commands_and_shortcuts
            else f'{command.description} {self._format_keybinding(command.keybinding)}'
        )
    
    def _command_rofi_input(self, command: Command) -> str:
        # TODO - add `meta` tag (b'\x1fmeta\x1fSOME_META')
        return f'{self._command_rofi_description(command)}\0info\x1f{command.identifier}'

    def _properly_sorted(self, commands: Iterable[Command]) -> List[Command]:
        """Sorts the commands first by their last used time, and then by lexical order"""
        sorting_key = lambda command: (-command.last_used.toordinal(), command.description.casefold())
        return sorted(commands, key=sorting_key)

    def _get_rofi_input(self, commands: Dict[CommandId, Command]) -> bytes:
        return '\n'.join([
            "\0prompt\x1fTODO - Choose a custom prompt",
            "\0message\x1fTODO - Choose a custom message",
            "\0no-custom\x1ftrue",
            *map(self._command_rofi_input, self._properly_sorted(commands.values()))
        ]).encode()
