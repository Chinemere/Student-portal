
# import os
# from flask import Flask, request, jsonify
# from flask_restx import Api, Resource, fields, Namespace
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
# from http import HTTPStatus
# from datetime import timedelta
# from werkzeug.security import generate_password_hash, check_password_hash

# basedir = os.path.dirname(os.path.realpath(__file__))
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'student.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
# app.config['SQLALCHEMY_ECHO']=True
# app.config['SCRET_KEY']= "8a0613f0fc102712ef0160ce05675df4db72ba33c89f22b27cb81e3bbdc50afa"
# app.config['JWT_SECRET_KEY']= "de7fa28f4cd2afb99c6e4c9dec79d318a4df75837c745c6a55b6adf813cd9f3e"
# app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=30)
# app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(minutes=30)
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()


# authorizations = {
#         "Bearer Auth": {
#             "type": "apiKey",
#             "in": "header",
#             "name": "Authorization",
#             "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize** "
#         }
#     }


# api = Api(app,doc='/')


# db=SQLAlchemy(app)
# migrate= Migrate(app, db)
# jwt = JWTManager(app)

# user_namespace = Namespace('users', description='namespace for users')
# auth_namespace = Namespace('auth', description='namespace for authentication', path='/auth')
# students_namespace = Namespace('students', description='namespace for students')
# teachers_namespace = Namespace('teachers', description='namespace for teachers')
# courses_namespace = Namespace('courses', description='namespace for courses')


# api.add_namespace(user_namespace)
# api.add_namespace(auth_namespace)
# api.add_namespace(students_namespace)
# api.add_namespace(teachers_namespace)
# api.add_namespace(courses_namespace)




# '''This is a function for calculating the student GP i.e Grade Point, 
# it is the summation of student test scores, assignment score,
# attendance and exam scores'''
# def gp( testScore1, attendanceScore1, assignmentScore1, examScore1):
#     aggregate = testScore1 + attendanceScore1 + assignmentScore1 + examScore1
#     return aggregate


# # Beginning of the Model section
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     username = db.Column(db.String(200), nullable=False)
#     passwordHash = db.Column(db.Text(200), nullable=False)
#     user_type = db.Column(db.String(50), nullable=False)

#     students = db.relationship("Student", backref="user_student")
#     teachers = db.relationship("Student", backref="user_teacher")


# class Student(db.Model):
#     __tablename__ = "students"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     matric_No = db.Column(db.Integer(), nullable=False)

#     course_id = db.Column(db.ForeignKey("course_tracks.id"))
#     user_id = db.Column(db.ForeignKey("users.id"))
#     student_results = db.relationship("StudentResult", backref="student")

#     def __repr__(self):
#         return self.name 
    

# class StudentResult(db.Model):
#     __tablename__ = "student_results"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     matric_No = db.Column(db.Integer(), nullable=False)
#     course = db.Column(db.String(200), nullable=False)
#     testScore = db.Column(db.Integer(), nullable=False)
#     attendanceScore = db.Column(db.Integer(), nullable=False)
#     assignmentScore = db.Column(db.Integer(), nullable=False)
#     examScore = db.Column(db.Integer(), nullable=False)
#     cGPA = db.Column(db.Integer())

#     student_id = db.Column(db.Integer, db.ForeignKey("students.id"))

#     def __repr__(self):
#         return self.name 


# class Teacher(db.Model):
#     __tablename__ = "teachers"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)

#     course_id = db.Column(db.ForeignKey("course_tracks.id"))
#     user_id = db.Column(db.ForeignKey("users.id"))
#     course = db.relationship("CourseTrack", backref="teacher")

#     def __repr__(self):
#         return self.name


# class CourseTrack(db.Model):
#     __tablename__ = "course_tracks"
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(300), nullable=False)

#     teacher_id = db.Column(db.ForeignKey("teachers.id"))
#     teacher = db.relationship("Teacher", backref="course")

#     def __repr__(self):
#         return self.title 


# def db_drop_create_all():
#     db.drop_all()
#     db.create_all()


# # model serialisation/ namespaces 
# student_model = students_namespace.model(
#     'Student', {
#         'id': fields.Integer(),
#         'name': fields.String(),
#         'email': fields.String(),
#         'matric_No': fields.Integer(),
#         'course': fields.String(),
#     }
# )

# studentResult_model = students_namespace.model(
#     'StudentResult', {
#         'id': fields.Integer(),
#         'name': fields.String(),
#         'email': fields.String(),
#         'matric_No': fields.Integer(),
#         'course': fields.String(),
#         'testScore' :fields.Integer(),
#         'attendanceScore' :fields.Integer(),
#         'assignmentScore' :fields.Integer(),
#         'examScore' :fields.Integer(),
#         'cGPA' :fields.Integer()
#     }
# )



# teacher_model = teachers_namespace.model(
#     'Teacher', {
#         'id': fields.Integer(),
#         'name': fields.String(),
#         'email': fields.String(),
#         'course': fields.String(),
#     }
# )

# track_model = teachers_namespace.model(
#     'CourseTrack', {
#         'id': fields.Integer(),
#         'title': fields.String(),
#         'teacher': fields.String(),
#     }
# )

# user_model = user_namespace.model(
#     'Users', {
#     "id":fields.Integer(description="An ID"),
#     "name":fields.String(description="Name of User"),
#     "email":fields.String(description="Email of user"),
#     "username":fields.String(description="username of the user"),
#     "passwordHash":fields.String(description="A Password"),

#     }
# )

# login_model = auth_namespace.model(
#     'Login', {
#     "email":fields.String(required=True, description="Email of user"),
#     "passwordHash":fields.String( required=True, description="A Password")

#     }
# )

# #end of model serialisation


# @app.shell_context_processor
# def make_shell_context():
#     return{
#         'db': db,
#         "Student":Student,
#         "StudentResult":StudentResult,
#         "Teacher": Teacher,
#         "CourseTrack": CourseTrack,
#         "db_drop_create_all": db_drop_create_all,
#         }




# # End of the Model section

# # Routes


# @api.route('/students')
# class CreateGetStudents(Resource):
#     @api.marshal_list_with(student_model, code= 200, envelope='students')
#     def get(self):
#         ''' Get all students '''
#         students = Student.query.all()
#         return students
    
#     @api.expect(student_model)
#     @api.marshal_with(student_model, code= 201, envelope='student')
#     def post(self):
#         ''' Create a new student account '''
#         data = request.get_json()
#         name = data.get('name')
#         email= data.get('email')
#         matric_No = data.get('matric_No')
#         course = data.get('course')
#         new_student = Student(name=name, email=email, matric_No=matric_No, course=course)
#         db.session.add(new_student)
#         db.session.commit()
#         return new_student



# @api.route('/student/<int:id>')
# class singleStudent(Resource):
#     @api.marshal_with(student_model, code= 200, envelope='student')
#     def get(self, id):
#         ''' Get A student by ID '''
#         student = Student.query.get_or_404(id)
#         return student, 200
    
#     @api.marshal_with(student_model, code= 200, envelope='student')
#     def put(self, id):
#         ''' Update all the information about a student account/datails '''
#         studentToUpdate = Student.query.get_or_404(id)
#         data = request.get_json()
#         studentToUpdate.name = data.get('name')
#         studentToUpdate.email = data.get('email')
#         studentToUpdate.matric_No = data.get('matric_No')
#         studentToUpdate.course = data.get('course')
#         db.session.commit()
#         return studentToUpdate
    
    
    
#     @api.marshal_with(student_model, code= 200, envelope='student_deleted')
#     def delete(self, id):
#         ''' Delete a student account/datails/record '''
#         studentToDelete = Student.query.get_or_404(id)
#         db.session.delete(studentToDelete)
#         db.session.commit()
#         return {'message': 'This student record has been deleted'}, 200


# #Teacher routes
# @api.route('/teachers')
# class Teachers(Resource):
#     @api.marshal_list_with(teacher_model, code= 200, envelope='teachers')
#     def get(self):
#         ''' Get all teacher '''
#         teacher = Teacher.query.all()
#         return teacher
    

#     @api.marshal_with(teacher_model, code= 201, envelope='teacher')
#     def post(self):
#         ''' Create a new Teacher record '''
#         data = request.get_json()
#         name = data.get('name')
#         email= data.get('email')
#         course = data.get('course')

#         new_teacher = Teacher(name=name, email=email, course=course)
#         db.session.add(new_teacher)
#         db.session.commit()
#         return new_teacher



# @api.route('/teacher/<int:id>')
# class singleTeacher(Resource):
#     @api.marshal_with(teacher_model, code= 200, envelope='teacher')
#     def get(self, id):
#         ''' Get A teacher by ID '''
#         teacher = Teacher.query.get_or_404(id)
#         return teacher, 200
    
#     @api.marshal_with(teacher_model, code= 200, envelope='teacher')
#     def put(self, id):
#         ''' Update all the information about a teacher account/datails '''
#         teacherToUpdate = Teacher.query.get_or_404(id)
#         data = request.get_json()
#         teacherToUpdate.name = data.get('name')
#         teacherToUpdate.email = data.get('email')
#         teacherToUpdate.course = data.get('course')
#         db.session.commit()
#         return teacherToUpdate
    
    
    
#     @api.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
#     def delete(self, id):
#         ''' Delete a teacher account/datails/record '''
#         teacherToUpdate = Teacher.query.get_or_404(id)
#         db.session.delete(teacherToUpdate)
#         db.session.commit()
#         return {'message': 'This teacher record has been deleted'}, 200
    


# #Track routes
# @api.route('/tracks')
# class Track(Resource):
#     @api.marshal_with(track_model, code= 200, envelope='tracks')
#     def get(self):
        
#         ''' Get all tracks '''
#         track = CourseTrack.query.all()
#         return track



#     @api.marshal_with(track_model, code= 201, envelope='track')
#     def post(self):
#         ''' Create a new track '''
#         data = request.get_json()
#         title = data.get('title')
#         teacher= data.get('teacher')

#         new_track = CourseTrack(title=title, teacher = teacher)
#         db.session.add(new_track)
#         db.session.commit()
#         return new_track
  
    
#     #get Track by id
# @api.route('/tracks/<int:id>')
# class Track(Resource):
#     @api.marshal_with(track_model, code= 200, envelope='tracks')
#     def get(self, id):
#         ''' Get one  track by id '''
#         track = CourseTrack.query.get_or_404(id)
#         return track


#     @api.marshal_with(track_model, code= 200, envelope='track')
#     def put(self, id):
#         ''' Update all the information about a track '''
#         TrackToUpdate = CourseTrack.query.get_or_404(id)
#         data = request.get_json()
#         TrackToUpdate.title = data.get('title')
#         TrackToUpdate.teacher = data.get('teacher')
#         db.session.commit()
#         return TrackToUpdate
    
#     @api.marshal_with(track_model, code= 200, envelope='track_deleted')
#     def delete(self, id):
#         ''' Delete a track '''
#         TrackToUpdate = CourseTrack.query.get_or_404(id)
#         db.session.delete(TrackToUpdate)
#         db.session.commit()
#         return {'message': 'This Track has been deleted'}, 200
    









# #Routs to get each student scores
# @students_namespace.route('/results')
# class StudentResults(Resource):
#     @api.marshal_list_with(studentResult_model, code= 200, envelope='studentScores')
#     def get(self):
#         ''' Get all student Results '''
#         studentResults = StudentResult.query.all()
#         return studentResults, HTTPStatus.CREATED
            


#     @students_namespace.expect(studentResult_model)
#     def post(self):
#         ''' insert a new student result '''
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')
#         matric_No = data.get('matric_No')
#         course = data.get('course')
#         testScore= data.get('testScore')
#         attendanceScore = data.get('attendanceScore')
#         assignmentScore = data.get('assignmentScore')
#         examScore = data.get('examScore')
#         cGPA = gp(testScore, attendanceScore, assignmentScore, examScore)
#         new_Result = StudentResult(
#             name=name, email=email, matric_No=matric_No, 
#             course=course,
#             testScore=testScore, 
#             attendanceScore=attendanceScore,
#             assignmentScore = assignmentScore, 
#             examScore = examScore,
#             cGPA = cGPA
#             )
#         db.session.add(new_Result)
#         db.session.commit()
#         return new_Result

# @students_namespace.route('/results/<int:id>')  
# class singleStudentResult(Resource):    
#     @students_namespace.marshal_with(studentResult_model, code= 201, envelope='studentScores')
#     def get(self, id):
#         ''' Get a student's result by id'''
#         studentResults = StudentResult.query.get_or_404(id)
#         return studentResults


#     @students_namespace.marshal_with(studentResult_model, code= 200, envelope='track')
#     @students_namespace.expect(studentResult_model)
#     def put(self, id):
#         ''' Update all the information about a student result '''
#         resultToUpdate = StudentResult.query.get_or_404(id)
#         data = request.get_json()
#         resultToUpdate.name = data.get('name')
#         resultToUpdate.email = data.get('email')
#         resultToUpdate.matric_No = data.get('matric_No')
#         resultToUpdate.course = data.get('course')
#         resultToUpdate.testScore = data.get('testScore')
#         resultToUpdate.attendanceScore = data.get('attendanceScore')
#         resultToUpdate.assignmentScore = data.get('assignmentScore')
#         resultToUpdate.examScore = data.get('examScore')
#         resultToUpdate.cGPA = gp(
#             resultToUpdate.testScore, 
#             resultToUpdate.attendanceScore, 
#             resultToUpdate.assignmentScore,  
#             resultToUpdate.examScore
#             )
#         db.session.commit()
#         return resultToUpdate
    
    
#     def delete(self, id):
#         ''' Delete a student Result '''
#         resultToDelete = StudentResult.query.get_or_404(id)
#         db.session.delete(resultToDelete)
#         db.session.commit()
#         return {'message': 'This student result has been deleted'}, 200
    




# # User routes
# @user_namespace.route('/users')
# class AllUsers(Resource):
#     @api.marshal_list_with(user_model, code= 200, envelope='allusers')
#     def get(self):
#         ''' Get all registed Users '''
#         allUsers = Users.query.all()
#         return allUsers, HTTPStatus.CREATED

# #sign up or create an accoung route
# @auth_namespace.route('/signup')
# class SignUp(Resource) :   
#     @auth_namespace.marshal_with(user_model, code= 200, envelope='new users')
#     @auth_namespace.expect(user_model)
#     @auth_namespace.doc(params={'name': "Your Name", 'email':'Your email', "username": "Your Username", "password": "Your Password"})
#     def post(self):
#         ''' Create an account'''
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')
#         username = data.get('username')
#         password = data.get('passwordHash')
#         new_user = Users(name=name, email=email, username=username, passwordHash=generate_password_hash(password))
#         db.session.add(new_user)
#         db.session.commit()
#         return new_user, HTTPStatus.CREATED
            

# #Login Routes
# @auth_namespace.route('/login')
# class Login(Resource) :   
#     @auth_namespace.expect(login_model)
#     @auth_namespace.doc(params={'email':'Your email', "password": "Your Password"})
#     def post(self):
#         ''' User Login '''
#         data = request.get_json()
#         email = data.get('email')
#         password =data.get('passwordHash')
#         users = Users.query.filter_by(email=email).first()
#         if (users is not None) and check_password_hash( users.passwordHash, password):
#             access_token= create_access_token(identity =users.username)
#             refresh_token = create_refresh_token(identity =users.username)

#             response = {
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#             }
#             return response, HTTPStatus.CREATED
       


# # End of Routes



# if __name__== '__main__':
#     app.run(debug=True, port=8000)