
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
migrate= Migrate(app, db)




def gp( testScore1, attendanceScore1, assignmentScore1, examScore1):
    aggregate = testScore1 + attendanceScore1 + assignmentScore1 + examScore1
    return aggregate


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


class CourseTrack(db.Model):
    __tablename__ = "course_track"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
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

track_model = api.model(
    'CourseTrack', {
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
        "Track": Track
        }




# End of the Model section
    
@api.route("/test")
class Test(Resource):
    def get(self):

        track = db.session.query(Track).all()
        return {"msg": f"{track}"}





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


#Teacher routes
@api.route('/teachers')
class Teachers(Resource):
    @api.marshal_list_with(teacher_model, code= 200, envelope='teachers')
    def get(self):
        ''' Get all teacher '''
        teacher = Teacher.query.all()
        return teacher
    

    @api.marshal_with(teacher_model, code= 201, envelope='teacher')
    def post(self):
        ''' Create a new Teacher record '''
        data = request.get_json()
        name = data.get('name')
        email= data.get('email')
        course = data.get('course')

        new_teacher = Teacher(name=name, email=email, course=course)
        db.session.add(new_teacher)
        db.session.commit()
        return new_teacher



@api.route('/teacher/<int:id>')
class singleTeacher(Resource):
    @api.marshal_with(teacher_model, code= 200, envelope='teacher')
    def get(self, id):
        ''' Get A teacher by ID '''
        teacher = Teacher.query.get_or_404(id)
        return teacher, 200
    
    @api.marshal_with(teacher_model, code= 200, envelope='teacher')
    def put(self, id):
        ''' Update all the information about a teacher account/datails '''
        teacherToUpdate = Teacher.query.get_or_404(id)
        data = request.get_json()
        teacherToUpdate.name = data.get('name')
        teacherToUpdate.email = data.get('email')
        teacherToUpdate.course = data.get('course')
        db.session.commit()
        return teacherToUpdate
    
    
    
    @api.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
    def delete(self, id):
        ''' Delete a teacher account/datails/record '''
        teacherToUpdate = Teacher.query.get_or_404(id)
        db.session.delete(teacherToUpdate)
        db.session.commit()
        return {'message': 'This teacher record has been deleted'}, 200
    


#Track routes
@api.route('/tracks')
class Track(Resource):
    @api.marshal_with(track_model, code= 200, envelope='tracks')
    def get(self):
        
        ''' Get all tracks '''
        track = CourseTrack.query.all()
        return track



    @api.marshal_with(track_model, code= 201, envelope='track')
    def post(self):
        ''' Create a new track '''
        data = request.get_json()
        title = data.get('title')
        teacher= data.get('teacher')

        new_track = CourseTrack(title=title, teacher = teacher)
        db.session.add(new_track)
        db.session.commit()
        return new_track
  
    
    #get Track by id
@api.route('/tracks/<int:id>')
class Track(Resource):
    @api.marshal_with(track_model, code= 200, envelope='tracks')
    def get(self, id):
        ''' Get one  track by id '''
        track = CourseTrack.query.get_or_404(id)
        return track


    @api.marshal_with(track_model, code= 200, envelope='track')
    def put(self, id):
        ''' Update all the information about a track '''
        TrackToUpdate = CourseTrack.query.get_or_404(id)
        data = request.get_json()
        TrackToUpdate.title = data.get('title')
        TrackToUpdate.teacher = data.get('teacher')
        db.session.commit()
        return TrackToUpdate
    
    @api.marshal_with(track_model, code= 200, envelope='track_deleted')
    def delete(self, id):
        ''' Delete a track '''
        TrackToUpdate = CourseTrack.query.get_or_404(id)
        db.session.delete(TrackToUpdate)
        db.session.commit()
        return {'message': 'This Track has been deleted'}, 200
    





#Routs to get each student scores
@api.route('/results')
class StudentResults(Resource):
    @api.marshal_list_with(studentResult_model, code= 200, envelope='studentScores')
    def get(self):
        ''' Get all student Results '''
        studentResults = StudentResult.query.all()
        return studentResults
            


    @api.marshal_with(studentResult_model, code= 201, envelope='studentScores')
    def post(self):
        ''' Create/insert a new student result '''
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        matric_No = data.get('matric_No')
        course = data.get('course')
        testScore= data.get('testScore')
        attendanceScore = data.get('attendanceScore')
        assignmentScore = data.get('assignmentScore')
        examScore = data.get('examScore')
        cGPA = gp(testScore, attendanceScore, assignmentScore, examScore)
        new_Result = StudentResult(
            name=name, email=email, matric_No=matric_No, 
            course=course,
            testScore=testScore, 
            attendanceScore=attendanceScore,
            assignmentScore = assignmentScore, 
            examScore = examScore,
            cGPA = cGPA
            )
        db.session.add(new_Result)
        db.session.commit()
        return new_Result

@api.route('/results/<int:id>')  
class singleStudentResult(Resource):    
    @api.marshal_with(studentResult_model, code= 201, envelope='studentScores')
    def get(self, id):
        ''' Get a student by id'''
        studentResults = StudentResult.query.get_or_404(id)
        return studentResults


    @api.marshal_with(studentResult_model, code= 200, envelope='track')
    def put(self, id):
        ''' Update all the information about a student result '''
        resultToUpdate = StudentResult.query.get_or_404(id)
        data = request.get_json()
        resultToUpdate.name = data.get('name')
        resultToUpdate.email = data.get('email')
        resultToUpdate.matric_No = data.get('matric_No')
        resultToUpdate.course = data.get('course')
        resultToUpdate.testScore = data.get('testScore')
        resultToUpdate.attendanceScore = data.get('attendanceScore')
        resultToUpdate.assignmentScore = data.get('assignmentScore')
        resultToUpdate.examScore = data.get('examScore')
        resultToUpdate.cGPA = gp(
            resultToUpdate.testScore, 
            resultToUpdate.attendanceScore, 
            resultToUpdate.assignmentScore,  
            resultToUpdate.examScore
            )
        db.session.commit()
        return resultToUpdate
    
    
    @api.marshal_with(track_model, code= 200, envelope='result_Deleted')
    def delete(self, id):
        ''' Delete a student Result '''
        resultToDelete = StudentResult.query.get_or_404(id)
        db.session.delete(resultToDelete)
        db.session.commit()
        return {'message': 'This student result has been deleted'}, 200
    





# End of Routes



if __name__== '__main__':
    app.run(debug=True, port=8000)