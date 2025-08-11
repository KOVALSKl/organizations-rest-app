from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class OrganizationFilterParams(BaseModel):
    building_id: Optional[int] = Query(None, description="Фильтрация по конкретному зданию")
    activity_id: Optional[int] = Query(None, description="Фильтрация по конкретному виду деятельности")


class OrganizationSearchParams(BaseModel):
    org_name: Optional[str] = Query(None, description="Поиск по названию организации")
    activity_name: Optional[str] = Query(None, description="Поиск по названию активности")
