from typing import List, Optional

from pydantic import BaseModel
from pydantic.schema import datetime


class TagBaseSchema(BaseModel):
    pass


class TagCreateSchema(TagBaseSchema):
    tag: str


class TagSchema(TagCreateSchema):
    id: int

    class Config:
        orm_mode = True


class TagDelSchema(TagCreateSchema):
    deleted_on: datetime | None

    class Config:
        orm_mode = True


class MeasureBaseSchema(BaseModel):
    pass


class MeasureCreateSchema(MeasureBaseSchema):
    measure: str


class MeasureSchema(MeasureCreateSchema):
    id: int

    class Config:
        orm_mode = True


class IngredientBaseSchema(BaseModel):
    pass


class IngredientCreateSchema(IngredientBaseSchema):
    name: str


class IngredientSchema(IngredientCreateSchema):
    id: int

    class Config:
        orm_mode = True


class IngredientCountSchema(BaseModel):
    id: int
    ingredient: IngredientSchema
    count: int
    measure: MeasureSchema

    class Config:
        orm_mode = True


class UserBaseSchema(BaseModel):
    pass


class UserSchema(UserBaseSchema):
    id: int
    first_name: str
    last_name: str


class RecipeBaseSchema(BaseModel):
    pass


class RecipeCreateSchema(RecipeBaseSchema):
    name: str
    description: str
    execute_time: int


class RecipeSchema(RecipeCreateSchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class RecipeFullSchema(RecipeCreateSchema):
    id: int
    user: UserSchema
    ingredients: List[IngredientCountSchema] | None
    tags: List[TagSchema] | None

    class Config:
        orm_mode = True
