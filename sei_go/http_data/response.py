from typing import Optional, Union, List

from sei_go.http_data.cookie import Cookie

class HTTPResponse:
    status_code: int
    content_type: Optional[str]
    body: bytes
    headers: dict
    cookies: List[Cookie]

    def __init__(self, 
                 status_code: int = 200,
                 content_type: str = None, 
                 body: Union[bytes, str] = b"",
                 cookies: List[Cookie] = None,
                 headers: dict = None):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        self.status_code = status_code
        self.content_type = content_type
        self.body = body
        self.headers = headers
        self.cookies = cookies