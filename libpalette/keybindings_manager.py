from typing import Iterable

from libpalette.command import Command

class KeybindingsManager:
    def load(self, keybindings: Iterable[Command]) -> None:
        raise NotImplementedError

    def __enter__(self) -> 'KeybindingsManager':
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        raise NotImplementedError
