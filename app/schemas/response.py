from typing import List

from pydantic import BaseModel, ConfigDict


class BuildingResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: str
    latitude: float
    longitude: float


class ActivityItemResponseSchema(BaseModel):
    id: int
    name: str


class ActivityClosureAncestorItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ancestor: ActivityItemResponseSchema


class ActivityClosureDescendantItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    descendant: ActivityItemResponseSchema


class ActivityResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    ancestors: List[ActivityClosureAncestorItemResponseSchema]
    descendants: List[ActivityClosureDescendantItemResponseSchema]


class OrganizationActivityResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PhoneResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone: str


class OrganizationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building: BuildingResponseSchema
    phones: List[PhoneResponseSchema]
    activities: List[OrganizationActivityResponseSchema]
