import logging.config

from customFramework.api import API
from webob import Request, Response

from customFramework.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


app = API()


@app.route(path='/home')
def home(request: Request, *args, **kwargs):
    response = Response()
    response.text = "Hello from the HOME page"
    return response


@app.route(path="/about")
def about(request: Request, *args, **kwargs):
    response = Response()
    response.text = "Hello from the ABOUT page"
    return response


@app.route(path="/say-my-name/{name}")
def about(request: Request, name, *args, **kwargs):
    response = Response()
    response.text = f"Hello {name}, wyd?"
    return response


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, num_1, num_2, *args, **kwargs):
    total = int(num_1) + int(num_2)
    response = Response()
    response.text = f"{num_1} + {num_2} = {total}"
    return response
