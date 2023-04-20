from typing import List, Sequence

from src.recipe.queries import get_recipe_sequences
from src.recipe.schemas import IngredientCountSchema, RecipeFullSchema, TagSchema


async def get_recipes_list(session, query_recipe_and_user, tag=None):
    sequences = await get_recipe_sequences(session, query_recipe_and_user, tag)

    return await create_recipes_list(*sequences)


async def add_key(elements) -> list | None:
    return elements if elements else None


async def get_list_ingredients(sequence, recipe_id) -> list:
    return [elem for elem in sequence if elem.recipe_id == recipe_id]


async def get_list_tags(sequence, recipe_id) -> list:
    return [elem.tag for elem in sequence if elem.recipe_id == recipe_id]


async def create_recipe_object(recipe, tags, ingredients) -> dict:
    return {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "execute_time": recipe.execute_time,
            "user": {
                "id": recipe.user.id,
                "first_name": recipe.user.first_name,
                "last_name": recipe.user.last_name,
            },
            "ingredients": await add_key(ingredients),
            "tags": await add_key(tags),
            "photos": [],
        }


async def create_recipes_list(list_recipes: Sequence,
                              list_ingredients_count: Sequence,
                              list_recipe_types: Sequence,
                              ) -> List[RecipeFullSchema] | list:

    recipes: List[RecipeFullSchema] | [None] = []

    for _recipe in list_recipes:

        add_tags: List[TagSchema] = await get_list_tags(list_recipe_types, _recipe.id)

        if not add_tags:
            continue

        add_ingredients: List[IngredientCountSchema] = await get_list_ingredients(list_ingredients_count, _recipe.id)
        recipe_item: dict = await create_recipe_object(_recipe, add_tags, add_ingredients)

        recipes.append(recipe_item)

    return recipes

