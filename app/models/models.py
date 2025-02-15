from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    edu_qualification = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    if_admin = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    result = db.relationship('Result', back_populates='user', cascade='all, delete-orphan')


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    unit=db.relationship('Unit', back_populates='subject',cascade= 'all, delete-orphan')


class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='unit')
    quiz = db.relationship('Quiz', back_populates='unit',cascade= 'all, delete-orphan')


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(100), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unit = db.relationship('Unit', back_populates='quiz')
    question = db.relationship('Question', back_populates='quiz',cascade= 'all, delete-orphan')
    result = db.relationship('Result', back_populates='quiz',cascade= 'all, delete-orphan')



class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    hints = db.Column(db.String(100), nullable=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', back_populates='question')



class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    time_of_attempt = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='result')
    quiz = db.relationship('Quiz', back_populates='result')