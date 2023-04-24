from http import HTTPStatus
from flask_restx import Namespace,Resource, abort, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models import CourseTrack, Student, StudentResult, User

students_namespace = Namespace('Students', description='namespace for students', path="/students")

# model serialisation/ namespaces 
student_model = students_namespace.model(
    'Student', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'course': fields.String(),
    }
)

# model serialisation/ namespaces 
update_student_model = students_namespace.model(
    'Student Update', {
        'name': fields.String(),
        'email': fields.String(),
    }
)

studentResult_model = students_namespace.model(
    'StudentResult', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'course': fields.String(),
        'testScore' :fields.Integer(),
        'attendanceScore' :fields.Integer(),
        'assignmentScore' :fields.Integer(),
        'examScore' :fields.Integer(),
        'cGPA' :fields.Integer()
    }
)

# This is a function for calculating the student GP i.e Grade Point, 
# it is the summation of student test scores, assignment score,
# attendance and exam scores
def gp( testScore1, attendanceScore1, assignmentScore1, examScore1):
    aggregate = testScore1 + attendanceScore1 + assignmentScore1 + examScore1
    return aggregate


@students_namespace.route('/')
class GetStudents(Resource):
    @students_namespace.marshal_list_with(student_model, code= 200, envelope='students')
    @jwt_required()
    def get(self):
        ''' Get all students '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            students = Student.query.all()
            return students, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


@students_namespace.route('/student/<int:id>')
class SingleStudent(Resource):
    @students_namespace.marshal_with(student_model, code= 200, envelope='student')
    @jwt_required()
    def get(self, id):
        ''' Get A student by ID '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            student = Student.query.get_or_404(id)
            return student, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")
    
    @students_namespace.expect(update_student_model)
    @students_namespace.marshal_with(student_model, code= 200, envelope='student')
    @jwt_required()
    def put(self, id):
        ''' Update all the information about a student account/datails '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            studentToUpdate = Student.query.get_or_404(id)
            data = request.get_json()

            studentToUpdate.name = data.get('name')
            studentToUpdate.email = data.get('email')

            studentToUpdate.update()
            return studentToUpdate, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")

    @students_namespace.marshal_with(student_model, code= 200, envelope='student_deleted')
    @jwt_required()
    def delete(self, id):
        ''' Delete a student account/datails/record '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            studentToDelete = Student.query.get_or_404(id)
            studentToDelete.delete()
            return {'message': 'This student record has been deleted'}, 200
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


@students_namespace.route("/results/student/<int:student_id>/course/<int:course_id>")
class AddRemoveStudentCourseResult(Resource): 
    @students_namespace.expect(studentResult_model)
    @students_namespace.marshal_with(studentResult_model)
    @jwt_required()
    def post(self, student_id, course_id):
        ''' Add a Course for Student '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            student = Student.get_by_id(student_id)
            course = CourseTrack.get_by_id(course_id)
            # checking if student and course id exist
            if student and course:
                add_course = StudentResult(
                    name=student.name, 
                    email=student.email, 
                    student_id=student.id,
                    course_id=course.id,
                    course_name=course.title
                    )
                add_course.save()

                student.course_id = course_id
                student.update()

                return add_course, HTTPStatus.CREATED
            abort(HTTPStatus.NOT_FOUND, "Student or Course ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


    @jwt_required()
    def delete(self, student_id, course_id):
        ''' Remove a Course for Student '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            student = Student.get_by_id(student_id)
            course = CourseTrack.get_by_id(course_id)
            student_course = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()
            # checking if student and course id exist
            if student and course:
                student_course.delete()

                return HTTPStatus.NO_CONTENT
            abort(HTTPStatus.NOT_FOUND, "Student or Course ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")
        
    
    def put(self, student_id, course_id):
        ''' insert a new student result '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            student = Student.get_or_404(student_id)
            course = Student.get_or_404(course_id)

            data = request.get_json()
            # checking if student and course id exist
            if student and course:
                student_course = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()
                if student_course:                
                    student_course.testScore=data.get('testScore'), 
                    student_course.attendanceScore=data.get('attendanceScore'),
                    student_course.assignmentScore = data.get('assignmentScore'), 
                    student_course.examScore=data.get('examScore')

                    # calculates and updates the cGPA
                    student_course.cGPA = gp(
                        student_course.testScore, 
                        student_course.attendanceScore, 
                        student_course.assignmentScore, 
                        student_course.examScore
                        )            
                    student_course.update()

                    return student_course, HTTPStatus.OK
                abort(HTTPStatus.NOT_FOUND, "Student not Registered for the Course")
            abort(HTTPStatus.NOT_FOUND, "Student or Course ID Not Found")
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


#Routs to get each student scores
@students_namespace.route('/results')
class GetStudentsResults(Resource):
    @students_namespace.marshal_list_with(studentResult_model, code= 200, envelope='studentScores')
    @jwt_required()
    def get(self):
        ''' Get all student Results '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            studentResults = StudentResult.query.all()
            return studentResults, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")

@students_namespace.route('/results/<int:id>')  
class GetSingleStudentResult(Resource):    
    @students_namespace.marshal_with(studentResult_model, code= 201, envelope='studentScores')
    @jwt_required()
    def get(self, id):
        ''' Get a student's result by id'''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            studentResults = StudentResult.query.get_or_404(id)
            return studentResults, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


@students_namespace.route('/student')
class GetCurrentStudent(Resource):
    @students_namespace.marshal_with(student_model, code= 200, envelope='student')
    @jwt_required()
    def get(self):
        ''' Get Current Student '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.user_type == 'student':
            student = Student.query.filter_by(user_id=current_user.id).first()
            return student, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Student have access")


@students_namespace.route('/student/results')  
class GetCurrentStudentResult(Resource):    
    @students_namespace.marshal_with(studentResult_model, code= 201, envelope='studentScores')
    @jwt_required()
    def get(self):
        ''' Get Current Student's Result '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        student = Student.query.filter_by(user_id=current_user.id)
        if current_user.user_type == 'student':
            studentResults = StudentResult.query.filter_by(student_id=student.id)
            return studentResults, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Student have access")
        
