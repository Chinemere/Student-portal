
import os
from flask import Flask
from flask_restx import Api, Namespace
from .models import db, User, Student, Teacher, StudentResult, CourseTrack, db_drop_create_all
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from http import HTTPStatus
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import auth_namespace
from .tracks import courses_namespace

basedir = os.path.dirname(os.path.realpath(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'student.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['SCRET_KEY']= "8a0613f0fc102712ef0160ce05675df4db72ba33c89f22b27cb81e3bbdc50afa"
app.config['JWT_SECRET_KEY']= "de7fa28f4cd2afb99c6e4c9dec79d318a4df75837c745c6a55b6adf813cd9f3e"
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(minutes=30)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize** "
    }
}


api = Api(app, doc='/')

db.init_app(app)
migrate= Migrate(app, db)
jwt = JWTManager(app)

user_namespace = Namespace('users', description='namespace for users')
# auth_namespace = Namespace('auth', description='namespace for authentication', path='/auth')
students_namespace = Namespace('students', description='namespace for students')
teachers_namespace = Namespace('teachers', description='namespace for teachers')



api.add_namespace(user_namespace)
api.add_namespace(auth_namespace)
api.add_namespace(students_namespace)
api.add_namespace(teachers_namespace)
api.add_namespace(courses_namespace)




'''This is a function for calculating the student GP i.e Grade Point, 
it is the summation of student test scores, assignment score,
attendance and exam scores'''
def gp( testScore1, attendanceScore1, assignmentScore1, examScore1):
    aggregate = testScore1 + attendanceScore1 + assignmentScore1 + examScore1
    return aggregate



#end of model serialisation


@app.shell_context_processor
def make_shell_context():
    return{
        'db': db,
        "Student":Student,
        "StudentResult":StudentResult,
        "Teacher": Teacher,
        "CourseTrack": CourseTrack,
        "db_drop_create_all": db_drop_create_all,
        }


if __name__== '__main__':
    app.run(debug=True, port=8000)