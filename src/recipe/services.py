from typing import List, Union, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.recipe.models import Recipe, Ingredient, Measure, IngredientCount, Tag, RecipeType
from src.recipe.schemas import IngredientCountSchema, RecipeFullSchema, TagSchema


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
    # except IntegrityError as e:
    #     result = await create_integrity_error(e)
    except Exception as e:
        result = await create_error(e)
    return result


async def get_recipes_list(session, query_recipe_and_user):  # query_recipe_and_user=select(Recipe, User).join(User)

    list_recipes = await get_sequence_from_db(session, query_recipe_and_user)

    recipe_ids = [recipe.id for recipe in list_recipes]
    query = select(
        IngredientCount, Ingredient, Measure
    ).join(
        Ingredient
    ).join(
        Measure
    ).filter(
        IngredientCount.recipe_id.in_(recipe_ids)
    )
    list_ingredients_count = await get_sequence_from_db(session, query)

    query = select(
        RecipeType, Tag
    ).join(
        Tag
    ).filter(
        RecipeType.recipe_id.in_(recipe_ids)
    )
    list_recipe_types = await get_sequence_from_db(session, query)

    recipes_list = await create_recipes_list(list_recipes,
                                             list_ingredients_count,
                                             list_recipe_types)

    return recipes_list


async def create_recipes_list(list_recipes: Sequence,
                              list_ingredients_count: Sequence,
                              list_recipe_types: Sequence,
                              ) -> Union[List[RecipeFullSchema] | list]:
    async def add_key(elements):
        return elements if elements else None

    recipes: List[RecipeFullSchema] | [None] = []

    for _recipe in list_recipes:
        add_ingredients: List[IngredientCountSchema] = [
            ingredient_element for ingredient_element
            in list_ingredients_count
            if ingredient_element.recipe_id == _recipe.id]

        add_tags: List[TagSchema] = [
            tag.tag for tag
            in list_recipe_types
            if all([tag.recipe_id == _recipe.id, tag.deleted_on is None])
        ]

        recipe_item: dict = {
            "id": _recipe.id,
            "name": _recipe.name,
            "description": _recipe.description,
            "execute_time": _recipe.execute_time,
            "user": {
                "id": _recipe.user.id,
                "first_name": _recipe.user.first_name,
                "last_name": _recipe.user.last_name,
            },
            "ingredients": await add_key(add_ingredients),
            "tags": await add_key(add_tags),
            "photos": [],
        }

        recipes.append(recipe_item)

    return recipes


async def create_error(e):
    return {
        "error": "error",
        "status": 500,
        "msg": e,
    }


async def create_integrity_error(e):
    return {
        "error": "error",
        "desc": "integrity_error",
        "status": 500,
        "msg": e.orig,
    }
