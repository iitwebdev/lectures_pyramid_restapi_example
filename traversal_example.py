from wsgiref.simple_server import make_server

from pyramid.view import view_config, view_defaults
from pyramid.config import Configurator


class PeopleResource(object):

    def __getitem__(self, people_id):
        if str(people_id).isdigit():
            return PersonResource(people_id)

    def __json__(self, request):
        return {
            'params': request.matchdict,
            'method': request.method,
        }


class PersonResource(PeopleResource):

    def __init__(self, people_id):
        self.id = people_id

    def __json__(self, request):
        return {
            'id': self.id,
            **super().__json__(request)
        }


class AnimalsResource(object):
    pass


@view_defaults(
    route_name='rest_api',
    renderer='json',
    context=PeopleResource
)
class RESTViewPeople(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        return self.context

    @view_config(request_method='POST')
    def post(self):
        return self.context

    @view_config(request_method='DELETE')
    def delete(self):
        return {'status': 'success'}


def rest_factory(request):
    return {
        'people': PeopleResource(),
        'animals': AnimalsResource(),
    }


if __name__ == '__main__':
    config = Configurator()
    config.add_route('rest_api', '/api/v1/*traverse', factory=rest_factory)
    config.add_view(RESTViewPeople, route_name='rest_api')
    config.scan('.')

    # make wsgi app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
