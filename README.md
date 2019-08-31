# Starlette-bugsnag

Bugsnag integration for Starlette ASGI framework.

Installation:
```
pip install starlette-bugsnag
```

Usage:
```python
from starlette_bugsnag import BugsnagMiddleware
import bugsnag

bugsnag.configure(...)

app = ...
app = BugsnagMiddleware(app)
```

Here's a more complete example using [Starlette](https://github.com/encode/starlette) and [uvicorn](https://github.com/encode/uvicorn):
```python

import bugsnag
import os
import uvicorn

from starlette_bugsnag import BugsnagMiddleware
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse

bugsnag.configure(api_key=os.getenv('BUGSNAG_API_KEY'), project_root=os.getcwd())

app = Starlette()
app.add_middleware(BugsnagMiddleware, debug=False)


@app.route("/")
def index(request):
    return PlainTextResponse("Hello World")


@app.route("/error")
def raiser(request):
    raise ValueError("This Is an Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

See [examples](examples) for more.
