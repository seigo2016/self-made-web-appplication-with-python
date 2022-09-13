import socket
from typing import final

class TCPServer:
    """
    A simple TCP server.
    """
    def __init__(self):
        pass

    def serve(self):
        """
        Serve the TCP server.
        """
        print("Start Server")
        # Create a TCP/IP socket
        try:
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('', 8080))
            server_socket.listen(10)

            print("Server is listening on port 8080")
            (client_socket, address) = server_socket.accept()
            print("Client connected from: ", address)

            request = client_socket.recv(4096)
            with open("data/server_recv.txt", "wb") as f:
                f.write(request)

            client_socket.close()

        finally:
            server_socket.close()
            print("Server is closed")

if __name__ == "__main__":
    server = TCPServer()
    server.serve()