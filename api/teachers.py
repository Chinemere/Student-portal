


# teacher_model = teachers_namespace.model(
#     'Teacher', {
#         'id': fields.Integer(),
#         'name': fields.String(),
#         'email': fields.String(),
#         'course': fields.String(),
#     }
# )


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
        teacherToUpdate.course = data.get('course')
#         db.session.commit()
#         return teacherToUpdate
    
    
    
#     @api.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
#     def delete(self, id):
#         ''' Delete a teacher account/datails/record '''
#         teacherToUpdate = Teacher.query.get_or_404(id)
#         db.session.delete(teacherToUpdate)
#         db.session.commit()
#         return {'message': 'This teacher record has been deleted'}, 200
    
