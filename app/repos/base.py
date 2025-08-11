from pydantic import BaseModel


class BaseRepo:
    def __init__(self):
        ...

    def get_item(self, item_id: int):
        ...

    def get_items(self, item_ids: list):
        ...

    def create(self, item: BaseModel):
        ...

    def update(self, item: BaseModel, data: BaseModel):
        ...

    def delete(self, item: BaseModel):
        ...