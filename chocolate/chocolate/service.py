from uuid import uuid4

import petname


class NotFoundException(Exception):
    pass


class Chocolate(object):
    def __init__(self, id=uuid4(), name=petname.generate(2)):
        self.id = id
        self.name = name


class ChocolateRepository(object):
    def create(self, chocolate: Chocolate) -> None:
        pass

    def get(self, uid) -> Chocolate:
        pass

    def list(self) -> [Chocolate]:
        pass

    def delete(self, uid) -> None:
        pass

    def update(self, chocolate: Chocolate) -> None:
        pass


class ChocolateService(object):

    def __init__(self, repository: ChocolateRepository) -> None:
        self.repository = repository

    def create(self, chocolate: Chocolate) -> None:
        chocolate.id = uuid4()
        self.repository.create(chocolate)

    def get(self, uid) -> Chocolate:
        return self.repository.get(uid)

    def list(self) -> [Chocolate]:
        return self.repository.list()

    def delete(self, uid) -> None:
        self.repository.delete(uid)

    def update(self, chocolate: Chocolate) -> None:
        self.repository.update(chocolate)



