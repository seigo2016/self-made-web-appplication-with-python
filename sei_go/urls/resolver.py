from typing import Callable, Optional

from sei_go.http_data.request import HTTPRequest
from sei_go.http_data.response import HTTPResponse
from sei_go.views.static import static
from urls import url_patterns

class URLResolver:
    def resolve(self, request: HTTPRequest) -> Callable[[HTTPRequest], HTTPResponse]:
        """
        Resolve url.
        """
        for url_pattern in url_patterns:
            match = url_pattern.match(request.path)
            if match:
                request.params.update(match.groupdict())
                return url_pattern.view
        return static