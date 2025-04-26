import datetime
import sqlalchemy
from .db_init import db
from sqlalchemy import orm

from werkzeug.security import *


class Classroom(db.Model):
    __tablename__ = 'classes'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    class_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))
    # ----------
    teacher = orm.relationship('Teacher')
    students = orm.relationship("Student", back_populates='classroom')
