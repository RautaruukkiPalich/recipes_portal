import datetime

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.db.pg.settings import get_async_session
from fastapi_cache.decorator import cache as redis_cache
from src.recipe.models import (Tag, Ingredient, Measure, Recipe)
from src.recipe.schemas import (TagCreateSchema, TagSchema, MeasureCreateSchema,
                                MeasureSchema, RecipeCreateSchema, IngredientCreateSchema,
                                IngredientSchema, RecipeFullSchema)
from src.recipe.queries import (get_sequence_from_db, post_sequence_to_db)
from src.recipe.services import get_recipes_list


router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)


@router.post("/tags/")
async def add_tag(
        tag_name: TagCreateSchema,
        session: AsyncSession = Depends(get_async_session)):

    query = select(Tag).where(tag_name.tag == Tag.tag)
    result = await get_sequence_from_db(session, query)
    if not result:
        stmt = insert(Tag).values(**tag_name.dict())
    else:
        stmt = update(Tag).where(tag_name.tag == Tag.tag).values(deleted_on=None)
    result = await post_sequence_to_db(session, stmt)

    return result


@router.get("/tags/", response_model=List[TagSchema])
# @redis_cache(expire=60)
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

    stmt = update(Tag).where(Tag.id == tag_id).values(deleted_on=None)
    result = await post_sequence_to_db(session, stmt)

    return result


@router.post("/measures/")
async def add_measure(
        measure_name: MeasureCreateSchema,
        session: AsyncSession = Depends(get_async_session)):

    query = select(Measure).where(Measure.measure == measure_name.measure)
    result = await get_sequence_from_db(session, query)

    if not result:
        stmt = insert(Measure).values(**measure_name.dict())
    else:
        stmt = update(Measure).where(Measure.measure == measure_name.measure).values(deleted_on=None)

    result = await post_sequence_to_db(session, stmt)

    return result


@router.get("/measures/", response_model=List[MeasureSchema])
# @redis_cache(expire=60)
async def get_measures(session: AsyncSession = Depends(get_async_session)):

    query = select(Measure)
    result = await get_sequence_from_db(session, query)

    return result


@router.post("/ingredients/")
async def add_ingredient(
        ingredient_name: IngredientCreateSchema,
        session: AsyncSession = Depends(get_async_session)):

    query = select(Ingredient).where(Ingredient.name == ingredient_name.name)
    result = await get_sequence_from_db(session, query)

    if not result:
        stmt = insert(Ingredient).values(**ingredient_name.dict())
    else:
        stmt = update(Ingredient).where(Ingredient.name == ingredient_name.name).values(deleted_on=None)

    result = await post_sequence_to_db(session, stmt)

    return result


@router.get("/ingredients/", response_model=List[IngredientSchema])
# @redis_cache(expire=60)
async def get_ingredients(session: AsyncSession = Depends(get_async_session)):

    query = select(Ingredient)
    result = await get_sequence_from_db(session, query)

    return result


@router.post("/")
async def add_recipe(
        recipe_items: RecipeCreateSchema,
        session: AsyncSession = Depends(get_async_session)):

    query = select(Recipe).where(Recipe.name == recipe_items.name)
    result = await get_sequence_from_db(session, query)

    if not result:
        stmt = insert(Recipe).values(**recipe_items.dict())
    else:
        stmt = update(Recipe).where(Recipe.name == recipe_items.name).values(deleted_on=None)

    result = await post_sequence_to_db(session, stmt)

    return result


@router.get("/", response_model=List[RecipeFullSchema])
# @redis_cache(expire=60)
async def get_full_recipes(
        tag: int | None = None,
        session: AsyncSession = Depends(get_async_session),
):

    query_recipe_and_user = select(Recipe, User).join(User)
    result = await get_recipes_list(session, query_recipe_and_user, tag)

    return result


@router.get("/{recipe_id}", response_model=RecipeFullSchema | None)
async def get_recipe_by_id(
        recipe_id: int,
        session: AsyncSession = Depends(get_async_session)):

    query_recipe_and_user = select(Recipe, User).join(User).where(Recipe.id == recipe_id)
    result = await get_recipes_list(session, query_recipe_and_user)

    return result[0] if result else None
