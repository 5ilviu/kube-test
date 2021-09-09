import tornado.ioloop
import tornado.web

from ice_cream import IceCream, IceCreams


def make_app():
    db = dict()
    return tornado.web.Application([
        (r"/ice-cream", IceCreams, dict(database=db)),
        (r"/ice-cream/(.*)", IceCream, dict(database=db)),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()