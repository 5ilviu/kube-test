import json
import random

import petname
import tornado.web


class IceCreamBase(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database
        self.database["1"] = ({"id": "1", "name": petname.generate(2)})


class IceCream(IceCreamBase):
    def get(self, uid):
        uid = str(uid)
        if uid in self.database:
            self.write({"ice_cream": self.database[uid]})
        else:
            self.send_error(404)

    def delete(self, uid):
        uid = str(uid)
        if uid in self.database:
            del self.database[uid]
            self.set_status(203)
        else:
            self.send_error(404)

    def put(self):
        pass


class IceCreams(IceCreamBase):
    def get(self):
        self.write({"items": [x for x in self.database.values()]})

    def post(self):
        print(self.request.body)
        ice_cream = json.loads(self.request.body.decode('utf-8'))
        ice_cream["id"] = str(random.randint(2, 1000))
        self.database[ice_cream["id"]] = ice_cream
        self.add_header("Location", "localhost:8888/ice-cream/{}".format(ice_cream["id"]))
        self.set_status(201)

