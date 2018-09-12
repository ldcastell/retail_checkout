from flask_restful import Resource, reqparse
from factory.db_factory import DBFactory


class BaseController(Resource):

    def __init__(self):
        self.req_parser = reqparse.RequestParser()
        self.dal_factory = DBFactory()

