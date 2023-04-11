import datetime

from pydantic import BaseModel


class TagBase(BaseModel):
    pass


class TagCreate(TagBase):
    tag: str


class Tag(TagBase):
    id: int
    tag: str

    class Config:
        orm_mode = True


class MeasureCreate(BaseModel):
    measure: str


class Measure(MeasureCreate):
    pass


class IngredientCreate(BaseModel):
    name: str


class Ingredient(IngredientCreate):
    pass
