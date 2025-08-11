from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload, with_loader_criteria

from app.db.models import Activity, ActivityClosure
from app.db.session import get_session
from app.schemas.base import BuildingModelSchema, ActivityModelSchema
from app.schemas.response import ActivityResponseSchema

router = APIRouter()


@router.get("/", response_model=List[BuildingModelSchema])
def get_activities():
    ...

@router.get("/{activity_id}", response_model=ActivityResponseSchema)
def get_activity(activity_id: int, session: Session = Depends(get_session)):
    activity = session.scalar(
        select(Activity)
        .options(
            joinedload(Activity.ancestors)
            .joinedload(ActivityClosure.ancestor),

            joinedload(Activity.descendants)
            .joinedload(ActivityClosure.descendant),

            with_loader_criteria(ActivityClosure, ActivityClosure.depth > 0)
        )
        .where(Activity.id == activity_id)
    )

    return activity


@router.post("/", response_model=ActivityResponseSchema)
def create_activity(activity: ActivityModelSchema, session: Session = Depends(get_session)):
    with session.begin():
        activity_obj = Activity(**activity.model_dump(exclude={"ancestors",}))
        session.add(activity_obj)
        session.flush()

        activity_closure = ActivityClosure.__table__

        self_link_insert_stmt = insert(ActivityClosure).values(
            ancestor_id = activity_obj.id,
            descendant_id = activity_obj.id,
            depth = 0
        ).on_conflict_do_nothing(index_elements=["ancestor_id", "descendant_id"])
        session.execute(self_link_insert_stmt)

        if activity.ancestors:
            ancestors_select = select(
                activity_closure.c.ancestor_id,
                bindparam("new_descendant_id"),
                (activity_closure.c.depth + 1).label("depth"),
            ).where(activity_closure.c.descendant_id.in_(activity.ancestors))

            ancestors_insert_stmt = insert(ActivityClosure.__table__).from_select(
                [ActivityClosure.ancestor_id, ActivityClosure.descendant_id, ActivityClosure.depth],
                ancestors_select,
            ).on_conflict_do_nothing(index_elements=["ancestor_id", "descendant_id"])

            session.execute(ancestors_insert_stmt, {"new_descendant_id": activity_obj.id})

    return activity_obj