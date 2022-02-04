import socket
from typing import Union, List

class Connection:
    _socket: socket.socket
    _closed: bool

    def __init__(self, connection_socket: socket.socket) -> None:
        self._socket = connection_socket
        self._closed = False

    def __enter__(self) -> 'Connection':
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if not self._closed:
            self.close()

    def close(self) -> None:
        self._socket.close()
        self._closed = True

    def send(self, message: Union[str, bytes]) -> None:
        self._socket.sendall(f'{message}\n'.encode() if isinstance(message, str) else message)
    
    def send_error(self, message: Union[str, bytes]) -> None:
        self.send(b'\x07' + (f'{message}\n'.encode() if isinstance(message, str) else message))
    
    def recv(self, buffsize: int = 4096) -> bytes:
        return self._socket.recv(buffsize)
    
    def recv_args(self) -> List[str]:
        return [arg.decode() for arg in self.recv().split(b'\0') if arg]
