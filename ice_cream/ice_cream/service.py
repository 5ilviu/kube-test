from uuid import uuid4

import petname


class NotFoundException(Exception):
    pass


class IceCream(object):
    def __init__(self, id=uuid4(), name=petname.generate(2)):
        self.id = id
        self.name = name


class IceCreamRepository(object):
    def create(self, chocolate: IceCream) -> None:
        pass

    def get(self, uid) -> IceCream:
        pass

    def list(self) -> [IceCream]:
        pass

    def delete(self, uid) -> None:
        pass

    def update(self, chocolate: IceCream) -> None:
        pass


class IceCreamService(object):

    def __init__(self, repository: IceCreamRepository) -> None:
        self.repository = repository

    def create(self, ice_cream: IceCream) -> None:
        ice_cream.id = uuid4()
        self.repository.create(ice_cream)

    def get(self, uid) -> IceCream:
        return self.repository.get(uid)

    def list(self) -> [IceCream]:
        return self.repository.list()

    def delete(self, uid) -> None:
        self.repository.delete(uid)

    def update(self, ice_cream: IceCream) -> None:
        self.repository.update(ice_cream)



