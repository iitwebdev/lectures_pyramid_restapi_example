from wsgiref.simple_server import make_server

from pyramid.view import view_config, view_defaults
from pyramid.config import Configurator


@view_defaults(
    route_name='rest_people',
    renderer='json'
)
class RESTViewPeople(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        return {
            'id': self.request.matchdict['id'],
            'method': self.request.method,
            'get': dict(self.request.GET)
        }

    @view_config(request_method='POST')
    def post(self):
        return {
            'id': self.request.matchdict['id'],
            'method': self.request.method,
            'post': dict(self.request.POST)
        }

    @view_config(request_method='DELETE')
    def delete(self):
        return {'status': 'success'}


if __name__ == '__main__':
    config = Configurator()
    config.add_route('rest_people', '/api/v1/people/{id:\d+}')
    config.add_view(RESTViewPeople, route_name='rest_people')
    config.scan('.')

    # make wsgi app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
