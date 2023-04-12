from pydantic import BaseModel
from pydantic.schema import datetime


class TagBase(BaseModel):
    pass


class TagCreate(TagBase):
    tag: str


class Tag(TagBase):
    id: int
    tag: str
    deleted_on: datetime | None

    class Config:
        orm_mode = True


class MeasureBase(BaseModel):
    pass


class MeasureCreate(MeasureBase):
    measure: str


class Measure(MeasureBase):
    id: int
    measure: str

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    pass


class IngredientCreate(IngredientBase):
    name: str


class Ingredient(IngredientBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    pass


class RecipeCreate(RecipeBase):
    name: str
    description: str
    execute_time: int
    user_id: int


class Recipe(RecipeBase):
    id: int
    name: str
    description: str
    execute_time: int
    user_id: int

    class Config:
        orm_mode = True
