from mongoengine import Document, StringField, UUIDField

import database
from ice_cream.ice_cream.service import IceCreamRepository, IceCream, NotFoundException


class IceCreamEntity(Document):
    id = UUIDField(primary_key=True)
    name = StringField()

    def as_ice_cream(self):
        return IceCream(self.id, self.name)


class IceCreamMongoRepository(IceCreamRepository):

    def create(self, ice_cream: IceCream) -> None:
        entity = IceCreamEntity(id=ice_cream.id, name=ice_cream.name)
        entity.save()

    def get(self, uid) -> IceCream:
        return IceCreamEntity.objects.get(id=uid).as_ice_cream()

    def list(self) -> [IceCream]:
        return list(map(lambda x: x.as_ice_cream(), IceCreamEntity.objects()))

    def delete(self, uid) -> None:
        IceCreamEntity.objects(id=uid).delete()

    def update(self, ice_cream: IceCream) -> None:
        ice_cream_entity = IceCreamEntity.objects.get(id=ice_cream.id)
        if ice_cream_entity is None:
            raise NotFoundException
        ice_cream_entity.name = ice_cream.name
        ice_cream_entity.save()

