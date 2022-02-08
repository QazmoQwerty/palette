from typing import Dict, Optional

from libpalette.configuration import get_configuration
from libpalette.command import Command, CommandId, CommandFactory, CommandIdFactory

class CommandsManager:
    _command_factory: CommandFactory
    _commands: Dict[CommandId, Command]

    def __init__(self) -> None:
        self.reload()
    
    def add_command(self, command: Command) -> None:
        self._commands[command.identifier] = command
    
    def get_command(self, identifier: CommandId) -> Optional[Command]:
        return self._commands.get(identifier)
    
    def get_commands(self) -> Dict[CommandId, Command]:
        return self._commands
    
    def reload(self) -> None:
        self._command_factory = CommandFactory(CommandIdFactory())
        self._commands = {}
        for i in get_configuration().data['commands']:
            self.add_command(self._command_factory.create(
                i['description'],
                i.get('keybinding'),
                i['exec'],
                i.get('meta')
            ))
