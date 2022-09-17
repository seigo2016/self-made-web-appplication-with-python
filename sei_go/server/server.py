import socket
from sei_go.server.worker import Worker

class Server:
    """
    A simple Web server.
    """

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
                thread = Worker(client_socket, address)
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
