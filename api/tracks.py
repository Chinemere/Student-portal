from http import HTTPStatus
from flask import request
from flask_restx import Resource, Namespace, fields, abort
from api.models import CourseTrack, Student, User
from flask_jwt_extended import jwt_required, get_jwt_identity

courses_namespace = Namespace('Courses', description='namespace for courses', path="/courses")


track_model = courses_namespace.model(
    'CourseTrack', {
        'id': fields.Integer(),
        'title': fields.String(),
        'teacher_id': fields.String(),
    }
)

course_students_model = courses_namespace.model(
    "Course Student", {
        "course_id": fields.Integer(),
        "student_name": fields.String()
       }
    )


#Track routes
@courses_namespace.route('/tracks')
class CreateGetTracks(Resource):
    @courses_namespace.marshal_with(track_model, code= 200, envelope='tracks')
    @jwt_required()
    def get(self):
        
        ''' Get all tracks '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            tracks = CourseTrack.query.all()
            return tracks
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")



    @courses_namespace.marshal_with(track_model, code= 201, envelope='track')
    @jwt_required()
    def post(self):
        ''' Create a new track '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            data = request.get_json()
            title = data.get('title')
            teacher_id= data.get('teacher_id')

            new_track = CourseTrack(title=title, teacher_id=teacher_id)
            new_track.save()

            return new_track, HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")

    
    #get Track by id
@courses_namespace.route('/tracks/<int:id>')
class GetUpdateDeleteTrack(Resource):
    @courses_namespace.marshal_with(track_model, code= 200, envelope='tracks')
    @jwt_required()
    def get(self, id):
        ''' Get one  track by id '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            track = CourseTrack.query.get_or_404(id)
            return track
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")


    @courses_namespace.marshal_with(track_model, code= 200, envelope='track')
    @jwt_required()
    def put(self, id):
        ''' Update all the information about a track '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            TrackToUpdate = CourseTrack.query.get_or_404(id)
            data = request.get_json()

            TrackToUpdate.title = data.get('title')
            TrackToUpdate.teacher_id = data.get('teacher_id')
            TrackToUpdate.update()
            return TrackToUpdate
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")

    
    @jwt_required()
    def delete(self, id):
        ''' Delete a track '''
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            TrackToUpdate = CourseTrack.query.get_or_404(id)
            TrackToUpdate.delete()
            return {'message': 'This Track has been deleted'}, 200
        abort(HTTPStatus.UNAUTHORIZED, "Only Admin have access")
    

@courses_namespace.route("/students/<int_course_id>")
class GetTrackStudents(Resource):
    @courses_namespace.marshal_with(course_students_model)
    def get(self, course_id):
        """ Get All STudent in a Track """
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.is_admin:
            track = CourseTrack.query.filter_by(course_id = course_id).first()
            if track:
                courseStudent = Student.query.filter_by(course_id=course_id).first()
                return courseStudent, HTTPStatus.OK
            abort(HTTPStatus.CONFLICT, )
