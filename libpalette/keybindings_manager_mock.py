from typing import Iterable

from libpalette.command import Command
from libpalette.keybindings_manager import KeybindingsManager

class KeybindingsManagerMock(KeybindingsManager):
    def load(self, keybindings: Iterable[Command]) -> None:
        pass

    def __enter__(self) -> 'KeybindingsManagerMock':
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        pass
