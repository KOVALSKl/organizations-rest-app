from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Building
from app.db.session import get_session
from app.schemas.base import BuildingModelSchema
from app.schemas.response import BuildingResponseSchema

router = APIRouter()


@router.get("/", response_model=List[BuildingModelSchema])
def get_buildings():
    ...

@router.get("/{building_id}")
def get_building(building_id: int, session: Session = Depends(get_session)):
    building = session.query(Building).get(building_id)

    print(building)

    if building is None:
        return None

    return {"address": building.address}

@router.post("/", response_model=BuildingResponseSchema)
def create_building(building: BuildingModelSchema, session: Session = Depends(get_session)):
    with session.begin():
        building_obj = Building(**building.model_dump())

        session.add(building_obj)
        session.commit()

    return building_obj