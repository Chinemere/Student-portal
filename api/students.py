



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
