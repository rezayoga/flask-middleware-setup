# This bluepint will deal with all user management functionality

from flask import Blueprint, request
from flask_restx import Api, Resource, fields

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY',
    }
}

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0.1', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})
DAO.create({'task': '!!!'})
DAO.create({'task': 'Ok!'})
DAO.create({'task': 'Siip!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


"""
api = Api(api_blueprint, version="1.0",
          title="Name Recorder",
          description="Manage names of various users of the application",
          authorizations=authorizations, security='apikey')

name_space = api.namespace('names', description='Manage names')

model = api.model('Name Model', {'name': fields.String(
    required=True, description="Name of the person", help="Name cannot be blank.")})

list_of_names = {}


@name_space.route("/<int:id>")
class MainClass(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, params={'id': 'Specify the Id associated with the person'})
    def get(self, id):
        try:
            name = list_of_names[id]
            return {
                "status": "Person retrieved",
                "name": list_of_names[id]
            }
        except KeyError as e:
            name_space.abort(
                500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(
                400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, params={'id': 'Specify the Id associated with the person'})
    @api.expect(model)
    def post(self, id):
        try:
            list_of_names[id] = request.json['name']
            return {
                "status": "New person added",
                "name": list_of_names[id]
            }
        except KeyError as e:
            name_space.abort(
                500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(
                400, e.__doc__, status="Could not save information", statusCode="400")
# Hide the full resource


@name_space.route('/resource1/', doc=False)
class Resource1(Resource):
    def get(self):
        return {}


@name_space.doc(security='apikey')
@name_space.route('/resource2/')
# @name_space.doc(False)
class Resource2(Resource):
    @api.doc(security='apikey')
    def get(self):
        key = request.headers.get('X-API-KEY')
        # print(key)
        if key != 'secret':
            return {}
        return f'Got {key} key'


@name_space.route('/resource3/')
# @name_space.hide
@name_space.doc(security='apikey')
class Resource3(Resource):
    def get(self):
        return {}

# Hide methods


@name_space.route('/resource4/')
@name_space.doc(delete=False)
class Resource4(Resource):
    def get(self):
        return {}

    @api.doc(False)
    def post(self):
        return {}

    @api.hide
    def put(self):
        return {}

    def delete(self):
        return {}
"""
