from http import HTTPStatus
from flask_restx import Namespace,Resource, fields
from flask import request

from api.models import Student, StudentResult

students_namespace = Namespace('Students', description='namespace for students', path="/students")

# model serialisation/ namespaces 
student_model = students_namespace.model(
    'Student', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'matric_No': fields.Integer(),
        'course': fields.String(),
    }
)

studentResult_model = students_namespace.model(
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

# '''This is a function for calculating the student GP i.e Grade Point, 
# it is the summation of student test scores, assignment score,
# attendance and exam scores'''
def gp( testScore1, attendanceScore1, assignmentScore1, examScore1):
    aggregate = testScore1 + attendanceScore1 + assignmentScore1 + examScore1
    return aggregate


@students_namespace.route('/students')
class CreateGetStudents(Resource):
    @students_namespace.marshal_list_with(student_model, code= 200, envelope='students')
    def get(self):
        ''' Get all students '''
        students = Student.query.all()
        return students, HTTPStatus.OK


@students_namespace.route('/student/<int:id>')
class SingleStudent(Resource):
    @students_namespace.marshal_with(student_model, code= 200, envelope='student')
    def get(self, id):
        ''' Get A student by ID '''
        student = Student.query.get_or_404(id)
        return student, HTTPStatus.OK
    
    @students_namespace.marshal_with(student_model, code= 200, envelope='student')
    def put(self, id):
        ''' Update all the information about a student account/datails '''
        studentToUpdate = Student.query.get_or_404(id)
        data = request.get_json()
        studentToUpdate.name = data.get('name')
        studentToUpdate.email = data.get('email')
        studentToUpdate.matric_No = data.get('matric_No')
        studentToUpdate.course = data.get('course')
        studentToUpdate.update()
        return studentToUpdate, HTTPStatus.OK

    @students_namespace.marshal_with(student_model, code= 200, envelope='student_deleted')
    def delete(self, id):
        ''' Delete a student account/datails/record '''
        studentToDelete = Student.query.get_or_404(id)
        studentToDelete.delete()
        return {'message': 'This student record has been deleted'}, 200


@students_namespace.route("/results/student/<int:student_id>/course/<int:course_id>")
class InsertStudentResult(Resource): 
    @students_namespace.expect(studentResult_model)
    def post(self, student_id, course_id):
        ''' insert a new student result '''
        student = Student.get_or_404(student_id)
        course = Student.get_or_404(course_id)

        data = request.get_json()
        # checking if student and course id exist
        if student and course:
            new_Result = StudentResult(
                name=student.name, 
                email=student.email, 
                matric_No=student.matric_No, 
                student_id=student.id,
                course_id=course.id,
                course_name=course.name,
                testScore= data.get('testScore'), 
                attendanceScore=data.get('attendanceScore'),
                assignmentScore = data.get('assignmentScore'), 
                examScore = data.get('examScore')
                )
            new_Result.save()

            # calculates and updates the cGPA
            new_Result.cGPA = gp(
                new_Result.testScore, 
                new_Result.attendanceScore, 
                new_Result.assignmentScore, 
                new_Result.examScore
                )            
            new_Result.update()
            return new_Result, HTTPStatus.CREATED


#Routs to get each student scores
@students_namespace.route('/results')
class StudentResults(Resource):
    @students_namespace.marshal_list_with(studentResult_model, code= 200, envelope='studentScores')
    def get(self):
        ''' Get all student Results '''
        studentResults = StudentResult.query.all()
        return studentResults, HTTPStatus.OK


@students_namespace.route('/results/<int:id>')  
class singleStudentResult(Resource):    
    @students_namespace.marshal_with(studentResult_model, code= 201, envelope='studentScores')
    def get(self, id):
        ''' Get a student's result by id'''
        studentResults = StudentResult.query.get_or_404(id)
        return studentResults, HTTPStatus.OK
