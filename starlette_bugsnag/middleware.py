import bugsnag

from .types import Scope, Receive, Send, ASGIApp


class BugsnagMiddleware:
    def __init__(self, app: ASGIApp, debug: bool = True) -> None:
        self.app = app
        self._debug = debug

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self._debug:
            await self.bugsnag_app(scope, receive, send)
            return
        await self.app(scope, receive, send)

    async def bugsnag_app(self, scope: Scope, receive: Receive, send: Send) -> None:
        bugsnag.configure_request(scope=scope)
        inner = self.app
        try:
            await inner(scope, receive, send)
        except Exception as exc:
            bugsnag.notify(exc)
            raise exc from None
        finally:
            bugsnag.clear_request_config()
