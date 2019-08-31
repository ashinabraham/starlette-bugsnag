import os

import bugsnag
import uvicorn
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import PlainTextResponse

from starlette_bugsnag import BugsnagMiddleware

config = Config('.env')
DEBUG = config.get("DEBUG", default=False)
BUGSNAG_API_KEY = config.get("BUGSNAG_API_KEY", default=None)

bugsnag.configure(api_key=BUGSNAG_API_KEY, project_root=os.getcwd())

app = Starlette(debug=DEBUG)
app.add_middleware(BugsnagMiddleware, debug=DEBUG)


@app.route("/")
def index(request):
    return PlainTextResponse("Hello World")


@app.route("/raise")
def raiser(request):
    raise ValueError("This Is an Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
