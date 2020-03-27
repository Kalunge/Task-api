from Models.userModel import UserModel, user_schema
from app import jwt_required, create_access_token, get_jwt_identity, api, fields, Resource
from werkzeug.security import generate_password_hash

register_namespace = api.namespace('register', description='Register new Users')
login_namespace = api.namespace('login', description='Authenticate already registered users')

regsiter_model = api.model('Register', {
    'full_name':fields.String(),
    'email' :fields.String(), 
    'password' :fields.String()
})

login_model = api.model('Login', {
    'email' :fields.String(), 
    'password' :fields.String()
})


@register_namespace.route('')
class UserRegister(Resource):
    @api.expect(regsiter_model)
    def post(self):
        data = api.payload
        email = data['email']
        user = UserModel(full_name=data['full_name'], email=email, password=generate_password_hash(data['password']))
        user.save_to_db()
        return user_schema.dump(user)


@login_namespace.route('')
class UserLogin(Resource):
    @api.expect(login_model)
    def post(self):
        data = api.payload
        email = data['email']
        user_id = UserModel.get_user_id(email)
        if UserModel.does_email_exists(email):
            if UserModel.validate_password(email, data['password']):
                return {'message':'login successful', 'access_token':create_access_token(identity=user_id)}
            else:
                return {'message':'Invalid login credentials'}
        else:
                return {'message':'Invalid login credentials'}

        