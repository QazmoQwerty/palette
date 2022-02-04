from libpalette.command import CommandId

class PaletteError(Exception):
    pass

class CommandNotFoundError(PaletteError):
    def __init__(self, identifier: CommandId) -> None:
        super().__init__(f'Command with identifier {identifier} does not exist')

class QuitException(Exception):
    def __init__(self) -> None:
        super().__init__('Quitting...')
