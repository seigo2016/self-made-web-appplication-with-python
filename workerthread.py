import os
import traceback
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple


class WorkerThread(Thread):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MIME_TYPES = {
        "html": "text/html",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpg",
        "gif": "image/gif",
    }

    def __init__(self, client_socket: socket, address: Tuple[str, int]):
        super().__init__()

        self.client_socket = client_socket
        self.client_address = address

    def run(self) -> None:
        self.handle_client()

    def handle_client(self) -> None:
        """
        Handle client.
        """
        request = self.client_socket.recv(4096)
        print(request)
        with open("data/server_recv.txt", "wb") as f:
            f.write(request)

        request_dict = self.parse_request(request)
        path = request_dict["path"]

        try:
            response_body = self.get_static_file(path)
            response_line = "HTTP/1.1 200 OK\r\n"
        except OSError:
            response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
            response_line = "HTTP/1.1 404 Not Found\r\n"
        
        response_header = self.gen_response_header(path, response_body)
        response = (response_line + response_header + "\r\n").encode() + response_body
        self.client_socket.send(response)

    def get_static_file(self, path:str) -> bytes:
        """
        Get static file.
        """

        relative_path = path[1:]
        static_file_path = os.path.join(self.STATIC_ROOT, relative_path)
        with open(static_file_path, "rb") as f:
            return f.read()

    def parse_request(self, request:bytes) -> dict:
        """
        Parse request.
        """
        print(request)
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

        method, path, http_version = request_line.decode().split(" ")

        return {
            "method": method,
            "path": path,
            "http_version": http_version,
            "request_header": request_header,
            "request_body": request_body,
        }

    def gen_response_header(self, path:str, response_body:bytes) -> str:
        """
        Generate response header.
        """
        if "." in path:
            ext = path.rsplit(".", maxsplit=1)[-1]
        else:
            ext = ""
        content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

        response_header = f"Date:{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Host: Seigo2016 Web Server/0.4\r\n"
        response_header += f"Content-Length: {len(response_body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {content_type}; charset=utf-8\r\n"
        return response_header