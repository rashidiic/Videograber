import json
from typing import Any
import httpx


class MockTransport(httpx.AsyncBaseTransport):
    def __init__(
        self, status_code: int = 200, response_data: dict[str, Any] | None = None
    ) -> None:
        self.status_code = status_code
        self.response_data = response_data or {"status": "ok"}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=self.status_code,
            content=json.dumps(self.response_data).encode(),
            request=request,
        )