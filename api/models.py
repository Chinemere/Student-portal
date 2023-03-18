from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

# Beginning of the Model section
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    passwordHash = db.Column(db.Text(200), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)

    students = db.relationship("Student", backref="user_student")
    teachers = db.relationship("Student", backref="user_teacher")

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    matric_No = db.Column(db.Integer(), unique=True, nullable=True)

    course_id = db.Column(db.ForeignKey("course_tracks.id"))
    user_id = db.Column(db.ForeignKey("users.id"))
    student_results = db.relationship("StudentResult", backref="student")

    def __repr__(self):
        return self.name
    
    def generate_matric(self, id):
        return f"STU{id:05}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    

class StudentResult(db.Model):
    __tablename__ = "student_results"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    matric_No = db.Column(db.Integer(), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course_tracks.id"))
    course_name = db.Column(db.String(200), nullable=False)
    testScore = db.Column(db.Integer(), nullable=False)
    attendanceScore = db.Column(db.Integer(), nullable=False)
    assignmentScore = db.Column(db.Integer(), nullable=False)
    examScore = db.Column(db.Integer(), nullable=False)
    cGPA = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return self.name 
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    user_id = db.Column(db.ForeignKey("users.id"))
    course = db.relationship("CourseTrack", backref="teacher")

    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


class CourseTrack(db.Model):
    __tablename__ = "course_tracks"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    teacher_id = db.Column(db.ForeignKey("teachers.id"))
    
    students = db.relationship("Student", backref="course")
    student_results = db.relationship("StudentResult", backref="course")

    def __repr__(self):
        return self.title 
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


def db_drop_create_all():
    db.drop_all()
    db.create_all()
