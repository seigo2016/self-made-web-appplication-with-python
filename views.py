import textwrap
from urllib import request, response
import urllib.parse
from datetime import datetime
from pprint import pformat
from typing import Tuple, Optional
from sei_go.http_data.request import HTTPRequest
from sei_go.http_data.response import HTTPResponse

def now() -> Tuple[bytes, Optional[str], str]:
    """Geneate a simple HTML page with the current time."""
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    body = textwrap.dedent(f"""\
        <h1>Current Time</h1>
        <p>The current time is {now_str}.</p>
        """)

    body = body.encode("utf-8")
    content_type = "text/html; charset=utf-8"
    return HTTPResponse(body=body, content_type=content_type, status_code=200)

def show_request(
    request: HTTPRequest
    ) -> HTTPResponse:
    """Generate a simple HTML page with the request information."""

    body = textwrap.dedent(f"""\
        <html>
        <body>
            <h1>Request Line:</h1>
            <p>
                {request.method} {request.path} {request.http_version}
            </p>
            <h1>Headers:</h1>
            <pre>{pformat(request.headers)}</pre>
            <h1>Body:</h1>
            <pre>{request.body.decode("utf-8", "ignore")}</pre>

        </body>
        </html>
    """)
    body = body.encode()
    content_type = "text/html; charset=utf-8"
    return HTTPResponse(body=body, content_type=content_type, status_code=200)

def parameters(
    request: dict
) -> Tuple[bytes, Optional[str], str]:
    """Generate a simple HTML page with the POST parameters."""
    if request.method == "GET":
        body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        content_type = "text/html; charset=UTF-8"
        status_code = 405
    elif request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        body = textwrap.dedent(f"""\
            <html>
            <body>
                <h1>Parameters:</h1>
                <pre>{pformat(post_params)}</pre>
            </body>
            </html>
        """)
        body = body.encode()
        content_type = "text/html; charset=utf-8"
        status_code = 200
    return HTTPResponse(body=body, content_type=content_type, status_code=status_code)


def user_profile(request: HTTPRequest) -> HTTPResponse:
    """Generate a simple HTML page with the user profile."""
    user_id = request.params["user_id"]
    body = textwrap.dedent(f"""\
        <html>
        <body>
            <h1>User Profile</h1>
            <p>User ID: {user_id}</p>
        </body>
        </html>
    """)
    body = body.encode()
    content_type = "text/html; charset=utf-8"
    return HTTPResponse(body=body, content_type=content_type, status_code=200)