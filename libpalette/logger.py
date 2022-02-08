
class Logger:
    _verbose: bool

    def __init__(self, verbose: bool) -> None:
        self._verbose = verbose
    
    def log(self, *args) -> None:
        if self._verbose:
            print(*args)
