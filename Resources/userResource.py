from Models.userModel import UserModel, users_schema, user_schema
from app import api, fields, Resource, get_jwt_identity
from Models.taskModel import TaskModel, tasks_schema

user_namespace = api.namespace('users', description='Endpoint for all operations concerning users')

user_model = api.model('User', {
    'full_name' :fields.String(),
    'email' :fields.String(),
    'password' :fields.String()
})


@user_namespace.route('')
class UserList(Resource):
    def get(self):
        """get all users"""
        users = UserModel.fetch_all()
        return users_schema.dump(users), 200

@user_namespace.route('/<int:id>')
class User(Resource):
    def get(self, id):
        user = UserModel.fetch_by_id(id)
        return user_schema.dump(user), 200

    @api.expect(user_model)   
    def put(self, id):
        user = UserModel.fetch_by_id(id)
        if user:
            if u'full_name' in data['full_name']:
                user.full_name = data['full_name']
            if u'email' in data['email']:
                user.email = data['email']
            return user_schema.dump(user), 200
        else:
            return {'message':'user does not exist'}, 404