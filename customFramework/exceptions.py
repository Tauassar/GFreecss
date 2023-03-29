
class DuplicateRoute(AssertionError):
    ...


class HTTPException(Exception):
    ...


class RouteNotFound(HTTPException):
    ...


class MethodNotAllowed(HTTPException):
    ...
