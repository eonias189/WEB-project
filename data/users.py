import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    register_date = sqlalchemy.Column(sqlalchemy.DATETIME)

    def set_password(self, password):
        self.hashed_password = password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> id: {self.id}; login: {self.login}; score: {self.score}'
