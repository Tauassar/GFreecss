import logging

from webob import Response
from webob import Request


logger = logging.getLogger(__name__)


class Middleware:
    def __init__(self, app) -> None:
        self.app = app

    def __call__(self, environ, start_response):
        return self.wsgi_application(environ, start_response)

    def add(self, middleware_cls) -> None:
        self.app = middleware_cls(self.app)

    def process_request(self, req):
        logger.debug('Hello, I\'m under the water')

    def process_response(self, req, resp):
        logger.debug('Please help me, here too much raining')

    def handle_request(self, request) -> Response:
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)
        return response

    def wsgi_application(self, environ, start_response) -> Response:
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)
