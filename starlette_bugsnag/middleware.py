import typing
from urllib import parse as urlparse

import bugsnag

from .types import Scope, Receive, Send, ASGIApp


class BugsnagMiddleware:
    def __init__(self, app: ASGIApp, debug: bool = True) -> None:
        self.app = app
        self._debug = debug

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self._debug:
            bugsnag.before_notify(self.additional_info)
            await self.bugsnag_app(scope, receive, send)
            return
        await self.app(scope, receive, send)

    async def bugsnag_app(self, scope: Scope, receive: Receive, send: Send) -> None:
        bugsnag.configure_request(scope=scope)
        inner = self.app
        try:
            await inner(scope, receive, send)
        except Exception as exc:
            bugsnag.configure_request(frame_locals=self.get_locals(exc))
            bugsnag.notify(exc)
            raise exc from None
        finally:
            bugsnag.clear_request_config()

    def get_locals(self, exception: Exception) -> typing.Dict:
        try:
            tb = exception.__traceback__
            while True:
                if tb.tb_next is not None:
                    tb = tb.tb_next
                else:
                    break
            return tb.tb_frame.f_locals
        except Exception as e:
            return {'error': 'Could not collect locals ({})'.format(e)}

    def get_url_info(self, scope: Scope) -> typing.Dict:
        scheme = scope.get("scheme", "http")
        path = scope.get("root_path", "") + scope["path"]
        query_string = scope["query_string"]
        server = scope.get("server", None)

        host_header = None
        headers = {}
        for key, value in scope["headers"]:
            if key == b"host":
                host_header = value.decode("latin-1")
            if key in headers:
                headers[key] = headers[key] + ", " + value
            else:
                headers[key] = value

        if host_header is not None:
            url = f"{scheme}://{host_header}{path}"
        elif server is None:
            url = path
        else:
            host, port = server
            default_port = {"http": 80, "https": 443, "ws": 80, "wss": 443}[scheme]
            if port == default_port:
                url = f"{scheme}://{host}{path}"
            else:
                url = f"{scheme}://{host}:{port}{path}"
        return {
            "url": url,
            "query": urlparse.unquote(query_string.decode("latin-1")),
            "headers": headers
        }

    def additional_info(self, notification) -> None:
        url_info = self.get_url_info(notification.request_config.scope)
        notification.add_tab("request", url_info)
        notification.add_tab("locals", notification.request_config.frame_locals)
