from http import HTTPStatus
from flask import request
from flask_restx import  Resource, Namespace, fields
from api.models import CourseTrack

courses_namespace = Namespace('Courses', description='namespace for courses', path="/courses")


track_model = courses_namespace.model(
    'CourseTrack', {
        'id': fields.Integer(),
        'title': fields.String(),
        'teacher_id': fields.String(),
    }
)


#Track routes
@courses_namespace.route('/tracks')
class CreateGetTracks(Resource):
    @courses_namespace.marshal_with(track_model, code= 200, envelope='tracks')
    def get(self):
        
        ''' Get all tracks '''
        track = CourseTrack.query.all()
        return track



    @courses_namespace.marshal_with(track_model, code= 201, envelope='track')
    def post(self):
        ''' Create a new track '''
        data = request.get_json()
        title = data.get('title')
        teacher= data.get('teacher_id')

        new_track = CourseTrack(title=title, teacher = teacher)
        new_track.save()

        return new_track, HTTPStatus.CREATED
  
    
    #get Track by id
@courses_namespace.route('/tracks/<int:id>')
class Track(Resource):
    @courses_namespace.marshal_with(track_model, code= 200, envelope='tracks')
    def get(self, id):
        ''' Get one  track by id '''
        track = CourseTrack.query.get_or_404(id)
        return track


    @courses_namespace.marshal_with(track_model, code= 200, envelope='track')
    def put(self, id):
        ''' Update all the information about a track '''
        TrackToUpdate = CourseTrack.query.get_or_404(id)
        data = request.get_json()

        TrackToUpdate.title = data.get('title')
        TrackToUpdate.teacher = data.get('teacher')
        TrackToUpdate.update()
        return TrackToUpdate
    
    @courses_namespace.marshal_with(track_model, code= 200, envelope='track_deleted')
    def delete(self, id):
        ''' Delete a track '''
        TrackToUpdate = CourseTrack.query.get_or_404(id)
        TrackToUpdate.delete()
        return {'message': 'This Track has been deleted'}, 200
    

