import datetime as dt
from flask_restful import abort, Resource
from flask import jsonify, request
from . import db_session
from .users import User
from .api_key_tools import check_key
from .parsers import UserPostParser, UserPutParser


def abort_if_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return abort(404, message=f'user {user_id} not found')


def abort_if_access_denied(request):
    if 'key' not in request.args or not check_key(request.method, request.args['key']):
        return abort(401, message='access denied')


USER_TO_DICT_ONLY = ('id', 'login', 'score', 'register_date')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_access_denied(request)
        abort_if_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=USER_TO_DICT_ONLY)})

    def delete(self, user_id):
        abort_if_access_denied(request)
        abort_if_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_access_denied(request)
        abort_if_not_found(user_id)
        parser = UserPutParser()
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        user.hashed_password = args['hashed_password'] if not args['hashed_password'] is None else user.hashed_password
        user.score = args['score'] if not args['score'] is None else user.score
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        abort_if_access_denied(request)
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [user.to_dict(only=USER_TO_DICT_ONLY) for user in users]})

    def post(self):
        abort_if_access_denied(request)
        parser = UserPostParser()
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).get(args['id']):
            return jsonify({'error': 'Id is already taken'})
        if db_sess.query(User).filter(User.login == args['login']).all():
            return jsonify({'error': 'Login is already taken'})
        user = User(id=args['id'], login=args['login'], hashed_password=args['hashed_password'],
                    score=args.get('score', 0), register_date=dt.datetime.now())
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
