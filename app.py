
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.dirname(os.path.realpath(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'student.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SQLALCHEMY_ECHO']=True


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


api = Api(app)
db=SQLAlchemy(app)




# Beginning of the Model section
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    matric_No = db.Column(db.Integer(), nullable=False)
    course = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return self.name 
    

class StudentResult(db.Model):
    __tablename__ = "studentResult"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    matric_No = db.Column(db.Integer(), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    testScore = db.Column(db.Integer(), nullable=False)
    attendanceScore = db.Column(db.Integer(), nullable=False)
    assignmentScore = db.Column(db.Integer(), nullable=False)
    examScore = db.Column(db.Integer(), nullable=False)
    cGPA = db.Column(db.Integer())

    def __repr__(self):
        return self.name 


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name


class Courses(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    teacher = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.title 
    






# model serialisation 


student_model = api.model(
    'Student', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'matric_No': fields.Integer(),
        'course': fields.String(),
    }
)

studentResult_model = api.model(
    'StudentResult', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'matric_No': fields.Integer(),
        'course': fields.String(),
        'testScore' :fields.Integer(),
        'attendanceScore' :fields.Integer(),
        'assignmentScore' :fields.Integer(),
        'examScore' :fields.Integer(),
        'cGPA' :fields.Integer()
    }
)



teacher_model = api.model(
    'Teacher', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'course': fields.String(),
    }
)

courses_model = api.model(
    'Courses', {
        'id': fields.Integer(),
        'title': fields.String(),
        'teacher': fields.String(),
    }
)

#end of model serialisation


@app.shell_context_processor
def make_shell_context():
    return{
        'db': db,
        "Student":Student,
        "StudentResult":StudentResult,
        "Teacher": Teacher,
        "Courses": Courses,
        }




# End of the Model section
    






# Routes
@api.route('/students')
class Students(Resource):
    @api.marshal_list_with(student_model, code= 200, envelope='students')
    def get(self):
        ''' Get all students '''
        students = Student.query.all()
        return students
    

    @api.marshal_with(student_model, code= 201, envelope='student')
    def post(self):
        ''' Create a new student account '''
        data = request.get_json()
        name = data.get('name')
        email= data.get('email')
        matric_No = data.get('matric_No')
        course = data.get('course')

        new_student = Student(name=name, email=email, matric_No=matric_No, course=course)
        db.session.add(new_student)
        db.session.commit()
        return new_student



@api.route('/student/<int:id>')
class singleStudent(Resource):
    @api.marshal_with(student_model, code= 200, envelope='student')
    def get(self, id):
        ''' Get A student by ID '''
        student = Student.query.get_or_404(id)
        return student, 200
    
    @api.marshal_with(student_model, code= 200, envelope='student')
    def put(self, id):
        ''' Update all the information about a student account/datails '''
        studentToUpdate = Student.query.get_or_404(id)
        data = request.get_json()
        studentToUpdate.name = data.get('name')
        studentToUpdate.email = data.get('email')
        studentToUpdate.matric_No = data.get('matric_No')
        studentToUpdate.course = data.get('course')
        db.session.commit()
        return studentToUpdate
    
    
    
    @api.marshal_with(student_model, code= 200, envelope='student_deleted')
    def delete(self, id):
        ''' Delete a student account/datails/record '''
        studentToDelete = Student.query.get_or_404(id)
        db.session.delete(studentToDelete)
        db.session.commit()
        return {'message': 'This student record has been deleted'}, 200

# End of Routes



if __name__== '__main__':
    app.run(debug=True, port=8000)