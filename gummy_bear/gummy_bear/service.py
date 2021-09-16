import uuid
from uuid import UUID

from pydantic import ValidationError, BaseModel, validator


class GummyBear(BaseModel):
    uid: UUID
    name: str
    color: str

    @validator('color')
    def color_validator(cls, value):
        if value.casefold() == 'blue':
            raise ValueError('no blue gummy bears please')
        return value

class GummyBearService(object):
    def create(self, gummy_bear: GummyBear) -> None:
        pass

    def get(self, uid) -> GummyBear:
        return GummyBear(uid=uuid.uuid4(), name='on the fly generated', color='red')

    def list(self, start=0, size=10) -> [GummyBear]:
        return [GummyBear(uid=uuid.uuid4(), name='on the fly generated', color='red')]

    def delete(self, uid) -> None:
        pass

    def update(self, gummy_bear: GummyBear) -> None:
        pass