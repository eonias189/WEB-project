import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Country(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'countries'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)
    complexity = sqlalchemy.Column(sqlalchemy.String)
    r = sqlalchemy.Column(sqlalchemy.Float)
    l = sqlalchemy.Column(sqlalchemy.Float)
    u = sqlalchemy.Column(sqlalchemy.Float)
    d = sqlalchemy.Column(sqlalchemy.Float)

    def __repr__(self):
        latitude = str(self.latitude) + ' с.ш.' if self.latitude > 0 else str(-self.latitude) + ' ю.ш.'
        longitude = str(self.longitude) + ' в.д.' if self.longitude > 0 else str(-self.longitude) + ' з.д.'
        return f'<{self.name}> {latitude} {longitude}'
