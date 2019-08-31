from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_bugsnag import BugsnagMiddleware


def test_success():
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        response = JSONResponse({"message": "success"})
        await response(scope, receive, send)

    server = BugsnagMiddleware(app, debug=True)
    client = TestClient(server, raise_server_exceptions=False)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_handler():
    async def app(scope, receive, send):
        raise RuntimeError("Something went wrong")

    server = BugsnagMiddleware(app, debug=True)
    client = TestClient(server, raise_server_exceptions=False)
    response = client.get("/")
    assert response.status_code == 500
