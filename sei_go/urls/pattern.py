import re
from re import Match
from typing import Callable, Optional

from sei_go.http_data.request import HTTPRequest
from sei_go.http_data.response import HTTPResponse

class URLPattern:
    pattern: str
    view: Callable[[HTTPRequest], HTTPResponse]

    def __init__(self, pattern: str, view: Callable[[HTTPRequest], HTTPResponse]):
        self.pattern = pattern
        self.view = view

    def match(self, path: str) -> Optional[Match]:
        """
        Match url.
        """
        pattern = self.pattern.replace("<", "(?P<").replace(">", ">[^/]+)")
        pattern = "^" + pattern + "$"
        return re.match(pattern, path)