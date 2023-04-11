from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.pg.settings import get_async_session
from src.recipe.models import (Tag as tag,
                               Ingredient as ingredient,
                               Measure as measure,
                               )
from src.recipe.schemas import TagCreate, IngredientCreate, MeasureCreate, Tag

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)


@router.post("/tag/")
async def add_tag(
        tag_name: TagCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(tag).values(**tag_name.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/measure/")
async def add_tag(
        measure_name: MeasureCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(measure).values(**measure_name.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/ingredient/")
async def add_tag(
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
    except IntegrityError:
        result = {
            "error": "IntegrityError",
            "status": 501,
        }
    return result


@router.get("/tag/", response_model=List[Tag])
async def get_recipes(session: AsyncSession = Depends(get_async_session)):
    query = select(tag)
    result = await session.scalars(query)
    return result.all()
