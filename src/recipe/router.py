import datetime

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.db.pg.settings import get_async_session
from src.recipe.models import (Tag, Ingredient, Measure, Recipe)
from src.recipe.schemas import (TagCreateSchema, TagSchema, MeasureCreateSchema,
                                MeasureSchema, RecipeCreateSchema, IngredientCreateSchema,
                                IngredientSchema, RecipeFullSchema)
from src.recipe.services import (get_sequence_from_db, get_recipes_list,
                                 post_sequence_to_db)

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)


@router.post("/tags/")
async def add_tag(
        tag_name: TagCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Tag).values(**tag_name.dict())
    result = await post_sequence_to_db(session, stmt)
    return result


@router.get("/tags/", response_model=List[TagSchema])
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    query = select(Tag)
    result = await get_sequence_from_db(session, query)
    return result


@router.delete("/tags/{tag_id}")
async def del_tag(
        tag_id: int,
        session: AsyncSession = Depends(get_async_session)):
    stmt = update(Tag).where(Tag.id == tag_id).values(deleted_on=datetime.datetime.now())
    result = await post_sequence_to_db(session, stmt)
    return result


@router.patch("/tags/{tag_id}")
async def patch_tag(
        tag_id: int,
        session: AsyncSession = Depends(get_async_session)):
    stmt = update(Tag) \
        .where(Tag.id == tag_id) \
        .values(deleted_on=None)
    result = await post_sequence_to_db(session, stmt)
    return result


@router.post("/measures/")
async def add_measure(
        measure_name: MeasureCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Measure).values(**measure_name.dict())
    result = await post_sequence_to_db(session, stmt)
    return result


@router.get("/measures/", response_model=List[MeasureSchema])
async def get_measures(session: AsyncSession = Depends(get_async_session)):
    query = select(Measure)
    result = await get_sequence_from_db(session, query)
    return result


@router.post("/ingredients/")
async def add_ingredient(
        ingredient_name: IngredientCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Ingredient).values(**ingredient_name.dict())
    result = await post_sequence_to_db(session, stmt)
    return result


@router.get("/ingredients/", response_model=List[IngredientSchema])
async def get_ingredients(session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient)
    result = await get_sequence_from_db(session, query)
    return result


@router.post("/")
async def add_recipe(
        recipe_items: RecipeCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Recipe).values(**recipe_items.dict())
    result = await post_sequence_to_db(session, stmt)
    return result


@router.get("/", response_model=List[RecipeFullSchema])
async def get_full_recipes(session: AsyncSession = Depends(get_async_session)):
    query_recipe_and_user = select(Recipe, User).join(User)
    result = await get_recipes_list(session, query_recipe_and_user)
    return result


@router.get("/{recipe_id}", response_model=RecipeFullSchema | None)
async def get_recipe_by_id(
        recipe_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    query_recipe_and_user = select(Recipe, User).join(User).where(Recipe.id == recipe_id)
    result = await get_recipes_list(session, query_recipe_and_user)
    return result[0] if result else None
