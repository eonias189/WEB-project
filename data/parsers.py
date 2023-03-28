from flask_restful import reqparse


class UserPostParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('id', required=True, type=int)
        self.add_argument('login', required=True)
        self.add_argument('hashed_password', required=True)
        self.add_argument('score', type=int)


class UserPutParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('hashed_password')
        self.add_argument('score', type=int)
