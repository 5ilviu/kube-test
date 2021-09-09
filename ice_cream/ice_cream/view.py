import json
import random
import uuid

import petname
import tornado.ioloop
import tornado.web

from ice_cream.ice_cream.model import IceCreamMongoRepository
from ice_cream.ice_cream.service import IceCream, IceCreamService, IceCreamRepository, NotFoundException


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NotFoundException:
            args[0].send_error(404)
    return inner_function


class IceCreamBaseView(tornado.web.RequestHandler):
    def initialize(self, service: IceCreamService):
        self.service = service

    def encode_ice_cream(self, v):
        return {'id': str(v.id), 'name': v.name}


class IceCreamView(IceCreamBaseView):
    @exception_handler
    def get(self, uid):
        uid = str(uid)
        ice_cream = self.service.get(uid)
        self.write(self.encode_ice_cream(ice_cream))

    @exception_handler
    def delete(self, uid):
        uid = uuid.UUID(uid)
        self.service.delete(uid)
        self.set_status(204)

    @exception_handler
    def put(self, uid):
        ice_cream = json.loads(self.request.body.decode('utf-8'), object_hook=lambda d: IceCream(**d))
        ice_cream.id = uid
        self.service.update(ice_cream)
        self.set_status(204)


class IceCreamsView(IceCreamBaseView):

    def get(self):
        self.write({"items": list(map(self.encode_ice_cream, self.service.list()))})

    def post(self):
        ice_cream = json.loads(self.request.body.decode('utf-8'), object_hook=lambda d: IceCream(**d))
        self.service.create(ice_cream)
        self.add_header("Location", "localhost:8888/ice-cream/{}".format(ice_cream.id))
        self.set_status(201)

def make_app():
    repository = IceCreamMongoRepository()
    service = IceCreamService(repository)
    return tornado.web.Application([
        (r"/ice-cream", IceCreamsView, dict(service=service)),
        (r"/ice-cream/(.*)", IceCreamView, dict(service=service)),
    ])


def start_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()