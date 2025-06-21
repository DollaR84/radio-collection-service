from typing import Any, Callable, Awaitable, Optional, MutableMapping

from bs4 import BeautifulSoup

from dishka import AsyncContainer

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class DishkaAdminMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, container: AsyncContainer):
        super().__init__(app)
        self.dishka_container = container

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        async with self.dishka_container() as container:
            request.state.container = container

            response = await call_next(request)
        return response


class InjectStaticMiddleware:

    def __init__(self, app: ASGIApp, js_urls: Optional[list[str]] = None, css_urls: Optional[list[str]] = None):
        self.app = app

        self.js_urls = js_urls or []
        self.css_urls = css_urls or []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        body_chunks = []
        status_code = 200
        headers: dict[bytes, bytes] = {}

        async def send_wrapper(message: MutableMapping[str, Any]) -> None:
            nonlocal status_code, headers

            if message["type"] == "http.response.start":
                headers = dict(message["headers"])
                status_code = message["status"]

            elif message["type"] == "http.response.body":
                body_chunks.append(message.get("body", b""))
                if not message.get("more_body", False):
                    body = b"".join(body_chunks)
                    content_type = b"text/html" in headers.get(b"content-type", b"")
                    if content_type:
                        html = body.decode("utf-8", errors="ignore")
                        soup = BeautifulSoup(html, "html.parser")

                        if soup.head:
                            for css_url in self.css_urls:
                                link = soup.new_tag("link", rel="stylesheet", href=css_url)
                                soup.head.append(link)

                        if soup.body:
                            for js_url in self.js_urls:
                                script = soup.new_tag("script", src=js_url)
                                soup.body.append(script)

                        new_body = str(soup).encode("utf-8")
                        new_headers = list(headers.items())
                        new_headers = [
                            (k, v) for k, v in new_headers if k.lower() != b"content-length"
                        ]
                        new_headers.append((b"content-length", str(len(new_body)).encode()))

                        await send({
                            "type": "http.response.start",
                            "status": status_code,
                            "headers": new_headers
                        })

                        await send({
                            "type": "http.response.body",
                            "body": new_body,
                            "more_body": False
                        })
                        return

                    await send({
                        "type": "http.response.start",
                        "status": status_code,
                        "headers": list(headers.items())
                    })

                    await send({
                        "type": "http.response.body",
                        "body": body,
                        "more_body": False
                    })
                    return

            else:
                await send(message)

        await self.app(scope, receive, send_wrapper)
