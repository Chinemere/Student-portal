from http import HTTPStatus
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Resource, abort, fields, Namespace
from .models import User, Student, Teacher, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Conflict, BadRequest





auth_namespace = Namespace('Auth', description='namespace for authentication', path='/auth')

login_model = auth_namespace.model(
    'Login', {
    "email":fields.String(required=True, description="Email of user"),
    "passwordHash":fields.String( required=True, description="A Password")

    }
)

user_model = auth_namespace.model(
    'Users', {
    "id":fields.Integer(description="An ID"),
    "name":fields.String(description="Name of User"),
    "email":fields.String(description="Email of user"),
    "username":fields.String(description="username of the user"),
    "password":fields.String(description="A Password"),
    "user_type": fields.String(description="User Type")
    }
)


user_teacher_model = auth_namespace.model(
    'Teachers', {
    "id":fields.Integer(description="An ID"),
    "name":fields.String(description="Name of User"),
    "email":fields.String(description="Email of user"),
    "username":fields.String(description="username of the user"),
    "user_type": fields.String(description="User Type")
    }
)


#sign up or create an accoung route
@auth_namespace.route('/signup')
class SignUp(Resource) :   
    @auth_namespace.marshal_with(user_teacher_model, code= 200, envelope='new users')
    @auth_namespace.expect(user_model)
    @auth_namespace.doc(params={'name': "Your Name", 'email':'Your email', "username": "Your Username", "password": "Your Password"})
    def post(self):
        ''' Create an account (Student, Teacher and Admin)'''
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user_type = data.get("user_type").lower()

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
    
        if email_exist:
            abort(HTTPStatus.CONFLICT, "Email already exist")
        elif username_exist:
            abort(HTTPStatus.CONFLICT, "Username already exist")
        else:
            new_user = User(name=name, email=email, username=username, user_type=user_type, passwordHash=generate_password_hash(password))
            new_user.save()
            if user_type == "student":
                new_student =  Student(name=name, email=email, user_id=new_user.id)
                new_student.save()
            elif user_type == "teacher":
                new_teacher = Teacher(name=name, email=email, user_id=new_user.id)
                new_teacher.save()
            elif user_type == "admin":
                new_admin = Admin(name=name, email=email, user_id=new_user.id)
                new_admin.save()
                
            return new_user, HTTPStatus.CREATED
        # abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")
            

#Login Routes
@auth_namespace.route('/login')
class Login(Resource) :   
    @auth_namespace.expect(login_model)
    @auth_namespace.doc(params={'email':'Your email', "password": "Your Password"})
    def post(self):
        ''' User Login '''
        "generate jwt pair"
        data = request.get_json()

        email = data.get('email')
        password =data.get('password')
        users = User.query.filter_by(email=email).first()
        if (users is not None) and check_password_hash(users.passwordHash, password):
            access_token= create_access_token(identity =users.username)
            refresh_token = create_refresh_token(identity =users.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        raise BadRequest("Invalid email or password")
       
@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required()
    def post(self):

        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)

        response = {
            "message": "Refresh Successful.",
            "access_token": access_token,
        }

        return response, HTTPStatus.CREATED


@auth_namespace.route("/users")
class GetUsers(Resource):
    """Get All Users"""
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        users = User.query.all()
        return users, HTTPStatus.OK