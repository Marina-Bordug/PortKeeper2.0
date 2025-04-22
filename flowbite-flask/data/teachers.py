import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import *


class Teacher(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)



def check_password(self, password):
    return check_password_hash(self.hashed_password, password)