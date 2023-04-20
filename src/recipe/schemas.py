from typing import List, Optional

from pydantic import BaseModel
from pydantic.schema import datetime


class EmptySchema(BaseModel):
    pass


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


class DataBaseSchema(BaseModel):
    pass


class DataCreateSchema(DataBaseSchema):
    pass


class DataSchema(DataBaseSchema):
    pass


class RecipeBaseSchema(BaseModel):
    pass


class RecipeSchema(BaseModel):
    id: int
    name: str
    description: str
    execute_time: int
    user_id: int

    class Config:
        orm_mode = True


class tmpSchema(BaseModel):
    ingredient: IngredientSchema
    count: int
    measure: MeasureSchema


class RecipeCreateSchema(RecipeBaseSchema):
    name: str
    description: str
    execute_time: int
    user_token: str
    # user_id: id
    ingredients: List[tmpSchema] | None
    tags: List[TagSchema] | None
    photos: List[DataSchema] | None


class RecipeFullSchema(RecipeBaseSchema):
    id: int
    name: str
    description: str
    execute_time: int
    user: UserSchema
    ingredients: List[IngredientCountSchema] | None
    tags: List[TagSchema] | None
    photos: List[DataSchema] | List[EmptySchema]

    class Config:
        orm_mode = True


