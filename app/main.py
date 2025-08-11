from fastapi import FastAPI

from app.routers.organization import router as organization_router
from app.routers.building import router as building_router
from app.routers.activity import router as activity_router

app = FastAPI()
app.include_router(organization_router, tags=["organizations"], prefix="/organizations")
app.include_router(building_router, tags=["buildings"], prefix="/buildings")
app.include_router(activity_router, tags=["activities"], prefix="/activities")


@app.get("/")
def read_root():
    return {"Hello": "World"}
