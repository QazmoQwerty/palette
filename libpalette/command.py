import random
import datetime
from dataclasses import dataclass
from typing import Optional, Union, Set

COMMAND_ID_SIZE = 4
COMMAND_ID_BASE = 10
MAX_COMMAND_ID = 10 ** COMMAND_ID_SIZE

class CommandId:
    value: int

    def __init__(self, value: Union[int, str]) -> None:
        self.value = value if isinstance(value, int) else int(value, COMMAND_ID_BASE)
    
    def __str__(self) -> str:
        return str(self.value).zfill(COMMAND_ID_SIZE)
    
    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.value == other.value
    
class CommandIdFactory:
    _existing_ids: Set[int]

    def __init__(self) -> None:
        self._existing_ids = set()
    
    def _get_unused_id(self) -> int:
        while True:
            r = random.randint(0, MAX_COMMAND_ID)
            if r not in self._existing_ids:
                return r
    
    def create(self, value: Optional[Union[int, str]] = None) -> CommandId:
        if value is None:
            value = self._get_unused_id()
        assert value not in self._existing_ids
        new_id = CommandId(value)
        self._existing_ids.add(new_id.value)
        return new_id

@dataclass
class Command:
    description: str
    exec_string: str
    identifier: CommandId
    keybinding: Optional[str] = None
    last_used: datetime.datetime = datetime.datetime.min

class CommandFactory:
    _id_factory: CommandIdFactory

    def __init__(self, id_factory: CommandIdFactory) -> None:
        self._id_factory = id_factory
    
    def create(self, description: str, keybinding: Optional[str], exec_string: str, identifier: Optional[Union[int, str]] = None) -> Command:
        return Command(description, exec_string, self._id_factory.create(identifier), keybinding)
