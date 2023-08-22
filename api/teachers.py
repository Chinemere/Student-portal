from http import HTTPStatus
from flask_restx import Namespace,Resource, fields, abort
from flask import request
from .tracks import track_model
from .models import User, Teacher
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models import Teacher

teachers_namespace = Namespace('teachers', description='namespace for teachers')

teacher_model = teachers_namespace.model(
    'Teacher', {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'course': fields.Nested(model=track_model),
    }
)


#Teacher routes
@teachers_namespace.route('/')
class GetTeachers(Resource):
    @teachers_namespace.marshal_list_with(teacher_model, code= 200, envelope='teachers')
    def get(self):
        ''' Get all teacher '''
        teacher = Teacher.query.all()
        return teacher

@teachers_namespace.route('/teacher/<int:id>')
class SingleTeacher(Resource):
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher')
    def get(self, id):
        ''' Get A teacher by ID '''
        teacher = Teacher.query.get_or_404(id)
        return teacher, 200


    @teachers_namespace.expect(teacher_model)
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher')
    @jwt_required()
    def put(self, id):
        ''' Update all the information about a teacher and their datails '''
        teacherToUpdate = Teacher.query.get_or_404(id)
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.user_type=="admin":
            data = request.get_json()
            teacherToUpdate.name = data.get('name')
            teacherToUpdate.email = data.get('email')
            teacherToUpdate.update()
            teacherToUpdate.name = data.get('name')
            teacherToUpdate.email = data.get('email')
            teacherToUpdate.update()
            return teacherToUpdate, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")
    
    
    
    
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
    @jwt_required()
    def delete(self, id):
        ''' Delete a teacher account/datails/record '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.user_type=="admin":
            teacherToDelete = Teacher.query.get_or_404(id)
            teacherToDelete.delete()
            return {'message': 'This Teacher record has been deleted'}, 200
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


























@teachers_namespace.route('/addteacher')
class AddATeacher(Resource):
    @teachers_namespace.expect(teacher_model)
    @teachers_namespace.marshal_with(teacher_model)
    @jwt_required()
    def post(self):
        """ Add A Teacher"""
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.user_type=="admin":
            data = request.get_json()
            name =data.get('name')
            email =data.get('email')
            # course =data.get('course')
            new_teacher = Teacher(name=name, email=email)
            new_teacher.save()
            return new_teacher, HTTPStatus.CREATED
        
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


       

      





    
    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher')
    def put(self, id):
        ''' Update all the information about a teacher account/datails '''
        teacherToUpdate = Teacher.query.get_or_404(id)
        data = request.get_json()

        teacherToUpdate.name = data.get('name')
        teacherToUpdate.email = data.get('email')
        teacherToUpdate.update()
        return teacherToUpdate

    @teachers_namespace.marshal_with(teacher_model, code= 200, envelope='teacher_deleted')
    def delete(self, id):
        ''' Delete a teacher account/datails/record '''
        teacherToDelete = Teacher.query.get_or_404(id)
        teacherToDelete.delete()
        return {'message': 'This teacher record has been deleted'}, 200
    
