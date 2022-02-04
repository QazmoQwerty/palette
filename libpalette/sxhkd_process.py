from signal import SIGUSR1
from typing import Optional
from subprocess import Popen

class SxhkdProcess:
    _process: Popen

    """
    """
    def __init__(self, *, count:        Optional[int] = None,
                          timeout:      Optional[int] = None,
                          config_file:  Optional[str] = None,
                          redir_file:   Optional[str] = None,
                          status_fifo:  Optional[str] = None,
                          abort_keysym: Optional[str] = None) -> None:
        args = ['sxhkd']
        if count        is not None: args += ['-m', str(count)  ]
        if timeout      is not None: args += ['-t', str(timeout)]
        if config_file  is not None: args += ['-c', config_file ]
        if redir_file   is not None: args += ['-r', redir_file  ]
        if status_fifo  is not None: args += ['-s', status_fifo ]
        if abort_keysym is not None: args += ['-a', abort_keysym]
        self._process = Popen(args)
    
    def reload_config(self) -> None:
        self._process.send_signal(SIGUSR1)
    
    def kill(self) -> None:
        self._process.kill()