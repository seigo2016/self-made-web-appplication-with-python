import os
import socket
from datetime import datetime
import os
class WebServer:
    """
    A simple Web server.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    
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

            request_line, remain = request.split(b"\r\n", maxsplit=1)
            request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

            method, path, http_version = request_line.decode().split(" ")

            relative_path = path[1:]
            static_file_path = os.path.join(self.STATIC_ROOT, relative_path)
            try:
                with open(static_file_path, "rb") as f:
                    response_body = f.read()

                response_line = "HTTP/1.1 200 OK\r\n"
            except OSError:
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_line = "HTTP/1.1 404 Not Found\r\n"

            response_header = f"Date:{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            response_header += "Host: Seigo2016 Web Server/0.2\r\n"
            response_header += f"Content-Length: {len(response_body)}\r\n"
            response_header += "Connection: Close\r\n"
            response_header += "Content-Type: text/html; charset=utf-8\r\n"
            
            response = (response_line + response_header + "\r\n").encode() + response_body

            client_socket.send(response)

            client_socket.close()
        finally:
            server_socket.close()
            print("Server is closed")

if __name__ == "__main__":
    server = WebServer()
    server.serve()