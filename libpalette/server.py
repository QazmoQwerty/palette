import os
import socket
from typing import Callable

from libpalette.utils import try_remove_file
from libpalette.connection import Connection
from libpalette.connection_handler import ConnectionHandler

class UnixSocketServer:
    _socket: socket.socket
    _socket_path: str
    _connection_handler: ConnectionHandler

    def __init__(self, socket_path: str, connection_handler: ConnectionHandler) -> None:
        self._socket = socket.socket(socket.AF_UNIX)
        self._socket_path = socket_path
        self._connection_handler = connection_handler
        
    def __enter__(self) -> 'UnixSocketServer':
        try_remove_file(self._socket_path)
        self._socket.bind(self._socket_path)
        self._socket.listen()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self._socket.close()
        try_remove_file(self._socket_path)

    def run(self) -> None:
        while True:
            with Connection(self._socket.accept()[0]) as connection:
                self._connection_handler.handle_connection(connection)
