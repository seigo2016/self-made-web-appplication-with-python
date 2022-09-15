import os
import traceback
from datetime import datetime
from socket import socket
from threading import Thread
from typing import Tuple
import textwrap
from pprint import pformat
import re

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
        with open("data/server_recv.txt", "wb") as f:
            f.write(request)

        request_dict = self.parse_request(request)
        path = request_dict["path"]
        if path == "/now":
            response_body, response_line, content_type = self.get_now()
            response_header = self.gen_response_header(path, response_body, content_type)

        elif path == "/show_request":
            response_body, response_line, content_type = self.get_show_request(request_dict)
            response_header = self.gen_response_header(path, response_body, content_type)

        else:
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
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)
        headers = {}
        for header_row in request_header.decode().split("\r\n"):
            key, value = re.split(r": *", header_row, maxsplit=1)
            headers[key] = value
        method, path, http_version = request_line.decode().split(" ")

        return {
            "method": method,
            "path": path,
            "http_version": http_version,
            "request_header": headers,
            "request_body": request_body,
        }

    def gen_response_header(self, path:str, response_body:bytes, content_type:str=None) -> str:
        """
        Generate response header.
        """
        if content_type is None:
            if "." in path:
                ext = path.rsplit(".", maxsplit=1)[-1]
            else:
                ext = ""
            content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

        response_header = f"Date:{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Host: Seigo2016 Web Server/0.5\r\n"
        response_header += f"Content-Length: {len(response_body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {content_type}; charset=utf-8\r\n"
        return response_header


    def get_now(self):
        html = f"""\
                    <html>
                    <body>
                        <h1>Now: {datetime.now()}</h1>
                    </body>
                    </html>
                """
        response_body = textwrap.dedent(html).encode()
        content_type = "text/html"
        response_line = "HTTP/1.1 200 OK\r\n"

        return response_body, response_line, content_type

    def get_show_request(self, request_dict:bytes):
        method = request_dict["method"]
        path = request_dict["path"]
        http_version = request_dict["http_version"]
        request_header = request_dict["request_header"]
        request_body = request_dict["request_body"]

        html = f"""\
                    <html>
                    <body>
                        <h1>Request Line:</h1>
                        <p>
                            {method} {path} {http_version}
                        </p>
                        <h1>Headers:</h1>
                        <pre>{pformat(request_header)}</pre>
                        <h1>Body:</h1>
                        <pre>{request_body.decode("utf-8", "ignore")}</pre>
                        
                    </body>
                    </html>
                """
        response_body = textwrap.dedent(html).encode()

        # Content-Typeを指定
        content_type = "text/html"

        # レスポンスラインを生成
        response_line = "HTTP/1.1 200 OK\r\n"
        return response_body, response_line, content_type