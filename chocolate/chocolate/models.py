from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID

from chocolate.chocolate.service import ChocolateRepository, Chocolate, NotFoundException
from database import Base, Session


class ChocolatePostgresRepository(ChocolateRepository):

    def create(self, chocolate: Chocolate) -> None:
        with Session() as session:
            session.add(ChocolateEntity(chocolate.id, chocolate.name))
            session.commit()

    def get(self, uid) -> Chocolate:
        with Session() as session:
            chocolate = session.query(ChocolateEntity).get(uid)
            if chocolate is None:
                raise NotFoundException("chocolate not found")
            return chocolate.as_chocolate()

    def list(self) -> [Chocolate]:
        with Session() as session:
            return list(map(ChocolateEntity.as_chocolate, session.query(ChocolateEntity).all()))

    def delete(self, uid) -> None:
        with Session() as session:
            entity = session.query(ChocolateEntity).get(uid)
            if entity is None:
                return  # todo add proper throws condition here
            session.delete(entity)
            session.commit()

    def update(self, chocolate: Chocolate) -> None:
        with Session() as session:
            entity = session.query(ChocolateEntity).get(chocolate.id)
            if entity is None:
                return  # todo add proper throws condition here
            entity.name = chocolate.name
            session.add(entity)
            session.commit()



class ChocolateEntity(Base):
    __tablename__ = 'chocolate'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def as_chocolate(self) -> Chocolate:
        return Chocolate(self.id, self.name)

