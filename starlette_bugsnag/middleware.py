import typing

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

    def additional_info(self, notification) -> None:
        notification.add_tab("locals", notification.request_config.frame_locals)
