import os
import re
from datetime import datetime
from socket import socket
from threading import Thread
import traceback
from typing import Tuple

import settings
from sei_go.http_data.response import HTTPResponse
from sei_go.http_data.request import HTTPRequest
from sei_go.urls.resolver import URLResolver

class Worker(Thread):
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
        try:
            request_bytes = self.client_socket.recv(4096)
            with open("data/server_recv.txt", "wb") as f:
                f.write(request_bytes)

            request = self.parse_request(request_bytes)
            
            view = URLResolver().resolve(request)

            response = view(request)

            response_header = self.gen_response_header(response, request)
            response_line = f"HTTP/1.1 {self.STATUS_LINES[response.status_code]}"
            response = (response_line + response_header + "\r\n").encode() + response.body
            self.client_socket.send(response)
        except Exception:
            print("Error")
            traceback.print_exc()
        
        finally:
            self.client_socket.close()
            print("Client is closed")

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
        response_header += "Host: Seigo2016 Web Server/0.8\r\n"
        response_header += f"Content-Length: {len(response.body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {response.content_type}; charset=utf-8\r\n"
        return response_header