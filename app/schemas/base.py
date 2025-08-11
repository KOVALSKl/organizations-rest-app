from pydantic import BaseModel, Field


class OrganizationModelSchema(BaseModel):
    name: str
    building_id: int
    phones: list[str]
    activities: list[int] | None = Field(default_factory=list, alias='activities')


class BuildingModelSchema(BaseModel):
    address: str
    latitude: float
    longitude: float


class ActivityModelSchema(BaseModel):
    name: str
    ancestors: list[int] | None = []


class PhoneModelSchema(BaseModel):
    organization_id: int
    phone: str