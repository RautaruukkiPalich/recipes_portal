from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.recipe.models import Ingredient, Measure, IngredientCount, Tag, RecipeType
from src.recipe.error_handlers import create_error


async def get_sequence_from_db(session: AsyncSession, query):
    result = await session.scalars(query)
    return result.all()


async def post_sequence_to_db(session: AsyncSession, stmt):
    try:
        await session.execute(stmt)
        await session.commit()
        result = {
            "error": None,
            "status": 200,
        }
    except Exception as e:
        result = await create_error(e)
    return result


async def get_recipe_sequences(session, query_recipe_and_user, tag=None):

    list_recipes = await get_sequence_from_db(session, query_recipe_and_user)

    recipe_ids = [recipe.id for recipe in list_recipes]

    query = select(
        IngredientCount, Ingredient, Measure
    ).join(
        Ingredient
    ).join(
        Measure
    ).where(
        IngredientCount.recipe_id.in_(recipe_ids)
    ).where(
        IngredientCount.deleted_on.is_(None)
    ).where(
        Ingredient.deleted_on.is_(None)
    ).where(
        Measure.deleted_on.is_(None)
    )
    list_ingredients_count = await get_sequence_from_db(session, query)

    query = select(
        RecipeType, Tag
    ).join(
        Tag
    ).where(
        RecipeType.recipe_id.in_(recipe_ids)
    ).where(
        Tag.deleted_on.is_(None)
    ).where(
        RecipeType.deleted_on.is_(None)
    )
    if tag:
        query = query.where(Tag.id == tag)
    list_recipe_types = await get_sequence_from_db(session, query)

    return [list_recipes, list_ingredients_count, list_recipe_types]

