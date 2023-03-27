import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    register_date = sqlalchemy.Column(sqlalchemy.DateTime)

    def set_password(self, password):
        self.hashed_password = password

    def check_password(self, password):
        return password == self.hashed_password

    def __repr__(self):
        return f'<User> {self.id} {self.login} {self.score}'
