import subprocess
from os import remove
from typing import Optional, Dict

from libpalette.utils import remove_whitespace
from libpalette.configuration import Configuration
from libpalette.command import Command, CommandId, COMMAND_ID_SIZE

class Rofi:
    _configuration: Configuration

    def __init__(self, configuration: Configuration) -> None:
        self._configuration = configuration
    
    def show_palette(self, commands: Dict[CommandId, Command]) -> Optional[CommandId]:
        result = subprocess.run(['rofi', '-dmenu', '-i', '-p', 'palette', '-no-custom'], stdout=subprocess.PIPE, input=self._get_rofi_input(commands))
        if result.returncode == 0 and result.stdout != b'\n':
            return CommandId(result.stdout.decode()[0:COMMAND_ID_SIZE])
        return None
    
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
        return f'{command.identifier}| ' + (
            command.description if command.keybinding is None
            else self._opposite_align(
                left = command.description,
                right = self._format_keybinding(command.keybinding),
                length = self._configuration.rofi_window_width
            ) if self._configuration.opposite_align_commands_and_shortcuts
            else f'{command.description} {self._format_keybinding(command.keybinding)}'
        )
    
    def _get_rofi_input(self, commands: Dict[CommandId, Command]) -> bytes:
        return '\n'.join(map(self._command_rofi_description,
            sorted(
                commands.values(),
                key=lambda command: (-command.last_used.toordinal(), command.description.casefold())
            )
        )).encode()