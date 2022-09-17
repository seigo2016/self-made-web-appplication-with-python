import os
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple
import re
from urls import URL_VIEW
from views import *
from http_data.response import HTTPResponse
from http_data.request import HTTPRequest

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
    STATUS_LINES = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }
    URL_VIEW = URL_VIEW

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
        request_bytes = self.client_socket.recv(4096)
        with open("data/server_recv.txt", "wb") as f:
            f.write(request_bytes)

        request = self.parse_request(request_bytes)
        content_type=""
        if request.path in self.URL_VIEW:
            view = self.URL_VIEW[request.path]
            response = view(request)
        else:
            try:
                response_body = self.get_static_file(request.path)
                content_type = None
                response = HTTPResponse(body=response_body, content_type=content_type, status_code=200)
            except OSError:
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                content_type="text/html; charset=UTF-8"
                response = HTTPResponse(body=response_body, content_type=content_type, status_code=404)
        response_header = self.gen_response_header(response, request)
        response_line = f"HTTP/1.1 {self.STATUS_LINES[response.status_code]}"
        response = (response_line + response_header + "\r\n").encode() + response.body
        self.client_socket.send(response)

    def get_static_file(self, path:str) -> bytes:
        """
        Get static file.
        """

        relative_path = path[1:]
        static_file_path = os.path.join(self.STATIC_ROOT, relative_path)
        with open(static_file_path, "rb") as f:
            return f.read()

    def parse_request(self, request:bytes) -> HTTPRequest:
        """
        Parse request.
        """
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)
        headers = {}
        for header_row in request_header.decode().split("\r\n"):
            key, value = re.split(r": *", header_row, maxsplit=1)
            headers[key] = value
        method, path, http_version = request_line.decode().split(" ")

        return HTTPRequest(method=method, 
                           path=path, 
                           http_version=http_version, 
                           headers=headers, 
                           body=request_body
                           )

    def gen_response_header(self, response: HTTPResponse, request: HTTPRequest) -> str:
        """
        Generate response header.
        """
        if response.content_type is None:
            if "." in request.path:
                ext = request.path.rsplit(".", maxsplit=1)[-1]
            else:
                ext = ""
            response.content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

        response_header = f"Date:{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Host: Seigo2016 Web Server/0.6\r\n"
        response_header += f"Content-Length: {len(response.body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {response.content_type}; charset=utf-8\r\n"
        return response_header