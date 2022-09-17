import socket
from urllib import response

class TCPClient:
    """
    A simple TCP client.
    """
    def __init__(self):
        pass

    def request(self):
        """
        Request the TCP server.
        """
        print("Start Client")
        # Create a TCP/IP socket
        try:
            client_socket = socket.socket()
            client_socket.connect(('localhost', 80))
            print("Client is connected to the server")

            with open("data/client_send.txt", "rb") as f:
                request = f.read()

            client_socket.send(request)
            print("Client sent the request")

            response = client_socket.recv(4096)
            with open("data/client_recv.txt", "wb") as f:
                f.write(response)
            client_socket.close()

        finally:
            print("Client is closed")

if __name__ == "__main__":
    client = TCPClient()
    client.request()