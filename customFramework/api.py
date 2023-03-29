import inspect
import logging
import os
from typing import Optional

from requests import Session as RequestsSession
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from parse import parse
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader

from customFramework import exceptions
from customFramework.exception_handlers import DefaultExceptionHandler

logger = logging.getLogger(__name__)


class API:
    _routes = {}
    templates_env: Environment = None
    exception_handler: callable = DefaultExceptionHandler.handle_exception
    whitenoise: WhiteNoise

    def __init__(self, templates_dir='templates', static_dir='static'):
        self._routes = {}
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )
        self.whitenoise = WhiteNoise(self.wsgi_application, root=static_dir)

    def wsgi_application(self, environ, start_response):
        request = Request(environ=environ)
        try:
            response = self.handle_request(request)

        except Exception as e:
            if self.exception_handler is None:
                raise e
            response = self.exception_handler(request=request, exception=e)

        return response(environ, start_response)

    def __call__(self, environ, start_response) -> Response:
        return self.whitenoise(environ, start_response)

    def set_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

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

    def handle_request(self, request) -> Response:
        response: Response
        handler, kwargs = self._get_route_handler(request.path)

        if handler:
            if inspect.isclass(handler):
                if hasattr(handler, request.method.lower()):
                    concrete_handler = getattr(handler(), request.method.lower())
                    response = concrete_handler(request, **kwargs)
                else:
                    raise exceptions.MethodNotAllowed(
                        f'Method {request.method} not allowed for {request.path}',
                    )
            else:
                response = handler(request, **kwargs)
        else:
            raise exceptions.RouteNotFound(f'No valid view for route {request.path} found')

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
