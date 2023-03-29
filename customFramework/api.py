import inspect
import logging
import os
from typing import Optional

from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from parse import parse
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader

from customFramework import exceptions

logger = logging.getLogger(__name__)


class API:
    _routes = {}
    templates_env: Environment = None

    def __init__(self, templates_dir='templates'):
        self._routes = {}
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def __call__(self, environ, start_response) -> Response:
        request = Request(environ=environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def _get_route_handler(self, route) -> tuple[Optional[callable], Optional[str]]:
        for path, handler in self._routes.items():
            parse_result = parse(path, route)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    @staticmethod
    def get_404_response() -> Response:
        response = Response()
        response.text = 'NOT FOUND'
        response.status = 404
        return response

    @staticmethod
    def get_405_response() -> Response:
        response = Response()
        response.text = 'METHOD NOT ALLOWED'
        response.status = 405
        return response

    def handle_request(self, request) -> Response:
        response: Response
        handler, kwargs = self._get_route_handler(request.path)

        if handler:
            if inspect.isclass(handler):
                if hasattr(handler, request.method.lower()):
                    concrete_handler = getattr(handler(), request.method.lower())
                    response = concrete_handler(request, **kwargs)
                else:
                    response = self.get_405_response()
            else:
                response = handler(request, **kwargs)
        else:
            response = self.get_404_response()

        logger.info(f'{request.method} {response.status} response for {request.path} route')
        return response

    def route(self, path):
        """Register route"""
        if path in self._routes:
            raise exceptions.DuplicateRoute("Such route already exists.")

        def wrapper(route_handler: callable, *args, **kwargs):
            self._routes[path] = route_handler
            return route_handler

        return wrapper
