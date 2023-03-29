import pytest
from webob import Response

from .exceptions import DuplicateRoute


def test_basic_route(api):
    @api.route('/home')
    def home(request):
        response = Response()
        response.text = 'TEST'
        return response


def test_route_overlap_throws_exception(api):
    @api.route('/home')
    def home(request):
        response = Response()
        response.text = 'TEST'
        return response

    with pytest.raises(DuplicateRoute):
        @api.route('/home')
        def home_2(request):
            response = Response()
            response.text = 'TEST2'
            return response


def test_client_can_send_requests(api, client):
    response_text = 'sample response'

    @api.route('/home')
    def home(request):
        response = Response()
        response.text = response_text
        return response

    assert client.request(method='GET', url='http://testserver/home').text == response_text


def test_response_status(api, client):
    @api.route('/home')
    def home(request):
        response = Response()
        response.text = ''
        return response

    assert client.request(method='GET', url='http://testserver/home').status_code == 200


def test_parametrized_routes(api, client):
    @api.route('/{name}')
    def home(request, name):
        response = Response()
        response.text = name
        return response

    for name in ['sasha', 'masha', 'pasha']:
        assert client.request(method='GET', url=f'http://testserver/{name}').text == name


def test_404_response(api, client):
    @api.route('/home')
    def home(request, name):
        response = Response()
        response.text = name
        return response

    response = client.request(method='GET', url=f'http://testserver/')

    assert response.text == 'NOT FOUND'
    assert response.status_code == 404


def test_cbv_post_response(api, client):
    @api.route("/book")
    class BooksResource:
        def get(self, request, *args, **kwargs):
            response = Response()
            response.text = "Books Page"
            return response

        def post(self, request, *args, **kwargs):
            response = Response()
            response.text = "Endpoint to create a book"
            response.status_code = 201
            return response

    response = client.request(method='POST', url=f'http://testserver/book')

    assert response.text == "Endpoint to create a book"
    assert response.status_code == 201


def test_cbv_get_response(api, client):
    @api.route("/book")
    class BooksResource:
        def get(self, request, *args, **kwargs):
            response = Response()
            response.text = "Books Page"
            return response

        def post(self, request, *args, **kwargs):
            response = Response()
            response.text = "Endpoint to create a book"
            response.status_code = 201
            return response

    response = client.request(method='GET', url=f'http://testserver/book')

    assert response.text == "Books Page"
    assert response.status_code == 200


def test_method_not_allowed_response(api, client):
    @api.route("/book")
    class BooksResource:
        def get(self, request, *args, **kwargs):
            response = Response()
            response.text = "Books Page"
            return response

        def post(self, request, *args, **kwargs):
            response = Response()
            response.text = "Endpoint to create a book"
            response.status_code = 201
            return response

    response = client.request(method='PUT', url=f'http://testserver/book')

    assert response.text == "METHOD NOT ALLOWED"
    assert response.status_code == 405
