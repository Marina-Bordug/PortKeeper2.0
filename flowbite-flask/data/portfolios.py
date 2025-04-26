import datetime
import sqlalchemy
from .db_init import db
from sqlalchemy import orm

from werkzeug.security import *


class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    level = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    result = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    student_name = orm.relationship('Student')
