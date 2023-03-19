import os
from flask import Flask
from flask_restx import Api
from .models import db, Student, Teacher, StudentResult, CourseTrack, db_drop_create_all
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from http import HTTPStatus
from datetime import timedelta
from .auth import auth_namespace
from .tracks import courses_namespace
from .students import students_namespace
from .teachers import teachers_namespace
from dotenv import load_dotenv
from .config import config_dict

# Load environment variables from .env file
load_dotenv()

def create_app(config=config_dict["dev"]):
    app=Flask(__name__) 

    app.config.from_object(config)   

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

    api.add_namespace(auth_namespace)
    api.add_namespace(students_namespace)
    api.add_namespace(teachers_namespace)
    api.add_namespace(courses_namespace)


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

    return app