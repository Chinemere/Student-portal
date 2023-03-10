
import os
from flask import Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.dirname(os.path.realpath(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'student.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SQLALCHEMY_ECHO']=True

api = Api(app)
db=SQLAlchemy(app)

@api.route('/students')
class Students(Resource):
    def get(self):
        ''' Get all students '''
        return {'message': 'These are all the students in the school'}
    
    def post(self):
        ''' Create a new student account '''
        return {'message': 'You have successfully created an account'}
    



@api.route('/student/<int:id>')
class Student(Resource):
    def get(self, id):
        ''' Get A student by ID '''
        return {'message': 'this is one student'}
    
    def put(self, id):
        ''' Update all the information about a student account/datails '''
        return {'message': 'You have successfully updated your details'}
    
    def patch(self, id):
        ''' Update some of the student account/datails '''
        return {'message': 'You have successfully updated  some of your your details'}
    
    def delete(self, id):
        ''' Delete a student account/datails '''
        return {'message': 'You have successfully deleted your details'}


if __name__== '__main__':
    app.run(debug=True, port=8000)