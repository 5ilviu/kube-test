from uuid import UUID

from fastapi import FastAPI
from pydantic.types import List

from service import GummyBearService, GummyBear

app = FastAPI()

service = GummyBearService()


@app.get("/gummy_bear/", response_model=List[GummyBear])
async def list_gummy_bears(start=0, size=10) -> List[GummyBear]:
    return service.list(start, size)


@app.get("/gummy_bear/{uid}", response_model=GummyBear)
async def get_gummy_bear(uid: UUID) -> GummyBear:
    return service.get(uid)


@app.post("/gummy_bear/", status_code=201, response_model=None)
async def create_gummy_bear(gummy_bear: GummyBear) -> None:
    service.create(gummy_bear)


@app.delete("/gummy_bear/{uid}", status_code=204, response_model=None)
async def delete_gummy_bear(uid: UUID) -> None:
    service.delete(uid)


@app.put("/gummy_bear/{uid}", status_code=204, response_model=None)
async def update_gummy_bear(gummy_bear: GummyBear, uid: UUID) -> None:
    if gummy_bear.uid != uid:
        raise ValueError('you mismatched the ids')
    service.update(gummy_bear)
