import os 
import traceback

import settings
from sei_go.http_data.request import HTTPRequest
from sei_go.http_data.response import HTTPResponse

def static(request: HTTPRequest) -> HTTPResponse:
    """
    Serve static files.
    """
    try:
        static_root = getattr(settings, "STATIC_ROOT")

        relative_path = request.path.lstrip("/")
        static_file_path = os.path.join(static_root, relative_path)
        with open(static_file_path, "rb") as f:
            response_body = f.read()

        content_type = None

        return HTTPResponse(body=response_body, content_type=content_type, status_code=200)

    except (OSError, FileNotFoundError):
        traceback.print_exc()
        response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
        content_type = "text/html; charset=UTF-8"
        return HTTPResponse(body=response_body, content_type=content_type, status_code=404)

    