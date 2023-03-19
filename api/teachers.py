from http import HTTPStatus
from flask_restx import Namespace,Resource, fields
from flask import request

from api.models import Teacher

teachers_namespace = Namespace('teachers', description='namespace for teachers')

teacher_model = teachers_namespace.model(
    'Teacher', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'course': fields.String(),
    }
)


#Teacher routes
@teachers_namespace.route('/teachers')
class GetTeachers(Resource):
    @teachers_namespace.marshal_list_with(teacher_model, code= 200, envelope='teachers')
    def get(self):
        ''' Get all teacher '''
        teacher = Teacher.query.all()
        return teacher
    


@teachers_namespace.route('/teacher/<int:id>')
class singleTeacher(Resource):
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher')
    def get(self, id):
        ''' Get A teacher by ID '''
        teacher = Teacher.query.get_or_404(id)
        return teacher, 200
    
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher')
    def put(self, id):
        ''' Update all the information about a teacher account/datails '''
        teacherToUpdate = Teacher.query.get_or_404(id)
        data = request.get_json()

        teacherToUpdate.name = data.get('name')
        teacherToUpdate.email = data.get('email')
        teacherToUpdate.course_id = data.get('course_id')
        teacherToUpdate.update()
        return teacherToUpdate
    
    
    
#     @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
#     def delete(self, id):
#         ''' Delete a teacher account/datails/record '''
#         teacherToUpdate = Teacher.query.get_or_404(id)
#         db.session.delete(teacherToUpdate)
#         db.session.commit()
#         return {'message': 'This teacher record has been deleted'}, 200
    
