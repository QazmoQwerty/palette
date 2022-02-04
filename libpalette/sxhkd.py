from typing import Iterable, Optional, overload

from libpalette.command import Command
from libpalette.utils import try_remove_file
from libpalette.sxhkd_process import SxhkdProcess
from libpalette.configuration import Configuration
from libpalette.keybindings_manager import KeybindingsManager

class Sxhkd(KeybindingsManager):
    _commands: Iterable[Command]
    _sxhkdrc_path: str
    _process: Optional[SxhkdProcess]

    def __init__(self, sxhkdrc_path: str) -> None:
        self._sxhkdrc_path = sxhkdrc_path
        self._commands = []
        self._process = None
    
    def _generate_sxhkdrc(self) -> str:
        return ''.join(
            f'# {c.description}\n{c.keybinding}\n    {c.exec_string}\n\n'
            for c in self._commands if c.keybinding is not None
        )

    def _dump_sxhkdrc(self) -> None:
        with open(self._sxhkdrc_path, 'w') as sxhkdrc_file:
            sxhkdrc_file.write(self._generate_sxhkdrc())
    
    def load(self, commands: Iterable[Command]) -> None:
        self._commands = commands
        if self._process is not None:
            self._dump_sxhkdrc()
            self._process.reload_config()
    
    def __enter__(self) -> KeybindingsManager:
        self._dump_sxhkdrc()
        self._process = SxhkdProcess(config_file = self._sxhkdrc_path)
        return self
        
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        assert self._process is not None
        self._process.kill()
        self._process = None
        try_remove_file(self._sxhkdrc_path)
