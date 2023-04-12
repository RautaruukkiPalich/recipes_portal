import datetime
import logging

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.pg.settings import get_async_session
from src.recipe.models import (Tag as tag,
                               Ingredient as ingredient,
                               Measure as measure,
                               Recipe as recipe,
                               )
from src.recipe.schemas import (TagCreate,
                                Tag,
                                MeasureCreate,
                                Measure,
                                RecipeCreate,
                                Recipe,
                                IngredientCreate,
                                Ingredient,
                                )

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)


async def create_integrity_error(e):
    return {
        "error": "error",
        "desc": "integrity_error",
        "status": 500,
        "msg": e.orig,
    }


async def create_error(e):
    return {
        "error": "error",
        "status": 500,
        "msg": e,
    }


@router.post("/tags/")
async def add_tag(
        tag_name: TagCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(tag).values(**tag_name.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/tags/", response_model=List[Tag])
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    query = select(tag)
    result = await session.scalars(query)
    return result.all()


@router.delete("/tags/")
async def del_tag(
        tag_id: int,
        session: AsyncSession = Depends(get_async_session)):
    stmt = update(tag)\
        .where(tag.id == tag_id)\
        .values(deleted_on=datetime.datetime.now())
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except IntegrityError as e:
        result = await create_integrity_error(e)
    except Exception as e:
        result = await create_error(e)
    return result


@router.patch("/tags/")
async def patch_tag(
        tag_id: int,
        session: AsyncSession = Depends(get_async_session)):
    stmt = update(tag)\
        .where(tag.id == tag_id)\
        .values(deleted_on=None)
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except IntegrityError as e:
        result = await create_integrity_error(e)
    except Exception as e:
        result = await create_error(e)
    return result


@router.post("/measures/")
async def add_measure(
        measure_name: MeasureCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(measure).values(**measure_name.dict())
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except IntegrityError as e:
        result = await create_integrity_error(e)
    except Exception as e:
        result = await create_error(e)
    return result


@router.get("/measures/", response_model=List[Measure])
async def get_measures(session: AsyncSession = Depends(get_async_session)):
    query = select(measure)
    result = await session.scalars(query)
    return result.all()


@router.post("/ingredients/")
async def add_ingredient(
        ingredient_name: IngredientCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(ingredient).values(**ingredient_name.dict())
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except IntegrityError as e:
        result = await create_integrity_error(e)
    except Exception as e:
        result = await create_error(e)
    return result


@router.get("/ingredients/", response_model=List[Ingredient])
async def get_ingredients(session: AsyncSession = Depends(get_async_session)):
    query = select(ingredient)
    result = await session.scalars(query)
    return result.all()


@router.post("/")
async def add_recipe(
        recipe_items: RecipeCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(recipe).values(**recipe_items.dict())
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except IntegrityError as e:
        result = await create_error(e)
    return result


@router.get("/", response_model=List[Recipe])
async def get_recipes(session: AsyncSession = Depends(get_async_session)):
    query = select(recipe)
    result = await session.scalars(query)
    return result.all()
