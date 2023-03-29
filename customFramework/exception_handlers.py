import logging

from webob import Response

from . import exceptions


logger = logging.getLogger(__name__)


class DefaultExceptionHandler:

    @classmethod
    def get_404_response(cls) -> Response:
        response = Response()
        response.text = 'NOT FOUND'
        response.status = 404
        return response

    @classmethod
    def get_405_response(cls) -> Response:
        response = Response()
        response.text = 'METHOD NOT ALLOWED'
        response.status = 405
        return response

    @classmethod
    def get_500_response(cls) -> Response:
        response = Response()
        response.text = 'INTERNAL SERVER ERROR'
        response.status = 500
        return response

    @classmethod
    def handle_exception(cls, request, exception, *args, **kwargs):
        if isinstance(exception, exceptions.RouteNotFound):
            return cls.get_404_response()

        elif isinstance(exception, exceptions.MethodNotAllowed):
            return cls.get_405_response()

        else:
            return cls.get_500_response()
