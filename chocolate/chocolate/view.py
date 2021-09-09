import json
import uuid

import tornado.ioloop
import tornado.web

from chocolate.chocolate.models import ChocolatePostgresRepository
from chocolate.chocolate.service import ChocolateService, Chocolate, NotFoundException


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NotFoundException:
            args[0].send_error(404)
    return inner_function


class ChocolateBaseView(tornado.web.RequestHandler):
    def initialize(self, service: ChocolateService):
        self.service = service

    def encode_chocolate(self, v):
        return {'id': str(v.id), 'name': v.name}


class ChocolateView(ChocolateBaseView):
    @exception_handler
    def get(self, uid):
        uid = str(uid)
        chocolate = self.service.get(uid)
        self.write(self.encode_chocolate(chocolate))

    def delete(self, uid):
        uid = uuid.UUID(uid)
        self.service.delete(uid)
        self.set_status(204)

    def put(self, uid):
        chocolate = json.loads(self.request.body.decode('utf-8'), object_hook=lambda d: Chocolate(**d))
        chocolate.id = uid
        self.service.update(chocolate)
        self.set_status(204)


class ChocolatesView(ChocolateBaseView):

    def get(self):
        self.write({"items": list(map(self.encode_chocolate, self.service.list()))})

    def post(self):
        chocolate = json.loads(self.request.body.decode('utf-8'), object_hook=lambda d: Chocolate(**d))
        self.service.create(chocolate)
        self.add_header("Location", "localhost:8888/chocolate/{}".format(chocolate.id))
        self.set_status(201)


def make_app():
    repository = ChocolatePostgresRepository()
    service = ChocolateService(repository)
    return tornado.web.Application([
        (r"/chocolate", ChocolatesView, dict(service=service)),
        (r"/chocolate/(.*)", ChocolateView, dict(service=service)),
    ])


def start_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()