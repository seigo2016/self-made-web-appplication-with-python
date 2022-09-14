import socket
from datetime import datetime

class WebServer:
    """
    A simple Web server.
    """
    def __init__(self):
        pass

    def serve(self):
        """
        Serve the Web server.
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

            response_body = "<html><body><h1>It works!</h1></body></html>"

            response_line = "HTTP/1.1 200 OK\r\n"

            response_header = f"Date:{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            response_header += "Host: Seigo2016 Web Server/0.1\r\n"
            response_header += f"Content-Length: {len(response_body.encode())}\r\n"
            response_header += "Connection: Close\r\n"
            response_header += "Content-Type: text/html; charset=utf-8\r\n"
            
            response = (response_line + response_header + "\r\n" + response_body).encode()

            client_socket.send(response)

            client_socket.close()

        finally:
            server_socket.close()
            print("Server is closed")

if __name__ == "__main__":
    server = WebServer()
    server.serve()