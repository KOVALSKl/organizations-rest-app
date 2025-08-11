from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload, with_loader_criteria, selectinload

from app.db.models import Organization, Phone, Activity, ActivityClosure, organization_activities
from app.db.session import get_session
from app.schemas.base import OrganizationModelSchema
from app.schemas.query import OrganizationFilterParams, OrganizationSearchParams
from app.schemas.response import OrganizationResponseSchema

router = APIRouter()


@router.get("/", response_model=List[OrganizationResponseSchema])
def get_organizations(filter_query: Annotated[OrganizationFilterParams, Query()], session: Session = Depends(get_session)):
    organizations = session.query(Organization)

    if filter_query.building_id:
        organizations = organizations.filter_by(building_id=filter_query.building_id)

    if filter_query.activity_id:
        organizations_filter_stmt = select(Organization).where(
            Organization.activities.any(Activity.id == filter_query.activity_id)
        )
        organizations = session.scalars(organizations_filter_stmt)

    return organizations.all()


@router.get("/search")
def search_organizations(
    search_query: Annotated[OrganizationSearchParams, Query()],
    session: Session = Depends(get_session)
):
    stmt = select(Organization).options(
        selectinload(Organization.activities),
        joinedload(Organization.building)
    )

    if search_query.org_name:
        stmt = stmt.where(Organization.name.ilike(f"%{search_query.org_name}%"))

    if search_query.activity_name:
        activity_match_subquery = select(Activity.id).where(Activity.name.ilike(f"%{search_query.activity_name}%")).subquery()

        descendants_subquery = (
            select(ActivityClosure.descendant_id)
            .where(ActivityClosure.ancestor_id.in_(activity_match_subquery))
            .where(ActivityClosure.depth > 0)
            .distinct()
            .subquery()
        )

        stmt = ((stmt.join(organization_activities, organization_activities.c.organization_id == Organization.id)
                .where(organization_activities.c.activity_id.in_(select(descendants_subquery.c.descendant_id))))
                .distinct())

    orgs = session.scalars(stmt).all()
    return orgs


@router.get("/{organization_id}", response_model=OrganizationResponseSchema)
def get_organization(organization_id: int, session: Session = Depends(get_session)):

    organization = session.scalar(
        select(Organization)
        .options(
            joinedload(Organization.activities)
            .joinedload(Activity.ancestors)
            .joinedload(ActivityClosure.ancestor),

            joinedload(Organization.activities)
            .joinedload(Activity.descendants)
            .joinedload(ActivityClosure.descendant),

            with_loader_criteria(ActivityClosure, ActivityClosure.depth > 0)
        )
        .where(Organization.id == organization_id)
    )

    return organization

@router.post("/", response_model=OrganizationResponseSchema)
def create_organization(organization: OrganizationModelSchema, session: Session = Depends(get_session)):
    with session.begin():
        organization_obj = Organization(
            **organization.model_dump(exclude={"phones", "activities"})
        )

        organization_obj.activities = session.scalars(
            select(Activity).where(Activity.id.in_(organization.activities))
        ).all()

        session.add(organization_obj)
        session.flush()

        phones = list(
            map(lambda phone: {
                "phone": phone,
                "organization_id": organization_obj.id,
            },
            organization.phones
        ))

        phones_insert_stmt = insert(Phone).values(phones)
        session.execute(phones_insert_stmt)

    return organization_obj
