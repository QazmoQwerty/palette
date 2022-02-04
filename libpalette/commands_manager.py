import json
from typing import Dict, Optional, Iterable

from libpalette.command import Command, CommandId, CommandFactory, CommandIdFactory

class CommandsManager:
    _commands_json_path: str
    _command_factory: CommandFactory
    _commands: Dict[CommandId, Command]

    def __init__(self, commands_json_path: str) -> None:
        self._commands_json_path = commands_json_path
        self.reload()
    
    def add_command(self, command: Command) -> None:
        self._commands[command.identifier] = command
    
    def get_command(self, identifier: CommandId) -> Optional[Command]:
        return self._commands.get(identifier)
    
    def get_commands(self) -> Dict[CommandId, Command]:
        return self._commands
    
    @staticmethod
    def _command_to_dict(command: Command) -> Dict[str, str]:
        result = {
            "description": command.description,
            "exec": command.exec_string,
        }
        if command.keybinding:
            result["keybinding"] = command.keybinding
        return result
    
    def store_commands(self) -> None:
        commands_list = list(map(CommandsManager._command_to_dict, self._commands.values()))
        with open(self._commands_json_path, 'w') as file:
            json.dump(commands_list, file, indent=4)
    
    def reload(self) -> None:
        self._command_factory = CommandFactory(CommandIdFactory())
        self._commands = {}
        with open(self._commands_json_path, 'r') as file:
            for i in json.load(file):
                self.add_command(self._command_factory.create(i['description'], i.get('keybinding'), i['exec']))
