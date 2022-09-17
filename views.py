import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat
from typing import Tuple, Optional
from sei_go.http_data.cookie import Cookie
from sei_go.http_data.request import HTTPRequest
from sei_go.http_data.response import HTTPResponse
from sei_go.template.renderer import render

def now(request: HTTPRequest) -> Tuple[bytes, Optional[str], str]:
    """Geneate a simple HTML page with the current time."""
    context = {"now": datetime.now()}
    body = render("now.html", context)
    return HTTPResponse(body=body)

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
        status_code = 405
        return HTTPResponse(body=body, status_code=status_code)
    elif request.method == "POST":
        context = {"params": urllib.parse.parse_qs(request.body.decode())}
        body = render("parameters.html", context)
        return HTTPResponse(body=body)


def user_profile(request: HTTPRequest) -> HTTPResponse:
    """Generate a simple HTML page with the user profile."""
    user_id = request.params["user_id"]
    context = {"user_id" : user_id}
    body = render("user_profile.html", context)
    return HTTPResponse(body=body)

def login(request: HTTPRequest) -> HTTPResponse:
    """Generate a simple HTML page with the login form."""
    if request.method == "GET":
        body = render("login.html", {})
        return HTTPResponse(body=body)

    elif request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        username = post_params["username"][0]
        email = post_params["email"][0]
        headers = {"Location": "/welcome"}
        cookies = [
            Cookie(name="username", value=username, max_age=30),
            Cookie(name="email", value=email, max_age=30),
        ]
        return HTTPResponse(status_code=302, headers=headers, cookies=cookies)

def welcome(request: HTTPRequest) -> HTTPResponse:
    if "username" not in request.cookies:
        print("redirect")
        headers = {"Location": "/login"}
        return HTTPResponse(status_code=302, headers=headers)

    username = request.cookies["username"]
    email = request.cookies["email"]
    context = {"username": username, "email": email}
    body = render("welcome.html", context)
    return HTTPResponse(body=body)

def set_cookie(request: HTTPRequest) -> HTTPResponse:
    return HTTPResponse(cookies={"username": "seigo"})