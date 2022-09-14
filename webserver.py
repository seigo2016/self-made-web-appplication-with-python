from importlib.resources import path
import os
import socket
from datetime import datetime
import os
import traceback
from workerthread import WorkerThread

class WebServer:
    """
    A simple Web server.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MIME_TYPES = {
        "html": "text/html",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpg",
        "gif": "image/gif",
    }
    def __init__(self):
        pass

    def serve(self):
        """
        Serve the Web server.
        """
        print("Start Server")
        # Create a TCP/IP socket
        try:
            server_socket = self.create_server_socket()
            print("Server is listening on port 8080")
            while True:
                (client_socket, address) = server_socket.accept()
                print("Client connected from: ", address)
                thread = WorkerThread(client_socket, address)
                thread.start()
        finally:
            server_socket.close()
            print("Server is closed")

    def create_server_socket(self) -> socket.socket:
        server_socket = socket.socket()          
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', 8080))
        server_socket.listen(10)
        return server_socket

if __name__ == "__main__":
    server = WebServer()
    server.serve()