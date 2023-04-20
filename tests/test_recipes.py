from copy import deepcopy

from httpx import AsyncClient


async def test_add_tag(ac: AsyncClient):
    data = {
        "tag": "custom_tag_name"
    }

    response = await ac.post("/recipes/tags/", json=data)
    assert response.status_code == 200


async def test_get_tags(ac: AsyncClient):
    response = await ac.get("/recipes/tags/", params=None)

    assert response.status_code == 200, "Тэги не поулчены"
    assert response.json()[0]["tag"] == "custom_tag_name", "Получен неправильный тэг"
    assert len(response.json()) == 1, "Получен НЕ один тэг"


async def test_del_tag(ac: AsyncClient):

    response = await ac.delete("/recipes/tags/1", params=None)

    assert response.status_code == 200, "Тэг не удалён"
    assert response.json().get("error") is None, "Ошибка в response"


async def test_patch_tag(ac: AsyncClient):

    response = await ac.patch("/recipes/tags/1", params=None)

    assert response.status_code == 200, "Тэг не восстановлен"
    assert response.json().get("error") is None, "Ошибка в response"


# MEASURES
async def test_add_measure(ac: AsyncClient):
    data = {
        "measure": "custom_measure_name"
    }

    response = await ac.post("/recipes/measures/", json=data)
    assert response.status_code == 200


async def test_get_measures(ac: AsyncClient):
    response = await ac.get("/recipes/measures/", params=None)

    assert response.status_code == 200, "Мера не поулчена"
    assert response.json()[0]["measure"] == "custom_measure_name", "Получена неправильная мера"
    assert len(response.json()) == 1, "Получена НЕ одна мера"


# INGREDIENTS
async def test_add_ingredients(ac: AsyncClient):
    data = {
        "name": "custom_ingredient_name"
    }

    response = await ac.post("/recipes/ingredients/", json=data)
    assert response.status_code == 200


async def test_get_ingredients(ac: AsyncClient):
    response = await ac.get("/recipes/ingredients/", params=None)

    assert response.status_code == 200, "Ингредиент не поулчен"
    assert response.json()[0]["name"] == "custom_ingredient_name", "Получен неправильный ингредиент"
    assert len(response.json()) == 1, "Получен НЕ один ингредиент"


#RECIPES

RECIPE_SAMPLE = {
        "id": 1,
        "name": "Блюдо",
        "description": "Описание",
        "execute_time": 25,
        "user": {
            "id": 1,
            "first_name": "first_name",
            "last_name": "last_name",
        },
        "ingredients": [
            {
                "id": 1,
                "ingredient": {
                    "name": "custom_ingredient_name",
                    "id": 1
                },
                "count": 2,
                "measure": {
                    "measure": "custom_measure_name",
                    "id": 1
                }
            }
        ],
        "tags": [
            {
                "tag": "custom_tag_name",
                "id": 1
            }
        ],
        "photos": [
        ]
    }


async def test_add_recipe(ac: AsyncClient):
    data = deepcopy(RECIPE_SAMPLE)
    data["photos"] = [{}]
    data["user_token"] = ""
    del data["user"]

    response = await ac.post("/recipes/", json=data)
    assert response.status_code == 200


async def test_get_recipe(ac: AsyncClient):
    response = await ac.get("/recipes/1", params={"recipe_id": 1})
    recipe = response.json()

    assert response.status_code == 200, "Рецепт не получен"
    assert len(recipe) == 8, "Получены не все элементы"
    assert recipe.get("id") == 1, "Некорректный id"
    assert recipe.get("name") == "Блюдо", "Некорректное название рецепта"
    assert recipe.get("description") == "Описание", "Некорректное описание"
    assert recipe.get("execute_time") == 25, "Некорректное время"
    assert recipe.get("user").get("id") == 1, "Некорректный id пользователя"
    assert recipe.get("ingredients")[0].get("id") == 1, "Некорректный id набора ингридиентов"
    assert recipe.get("ingredients")[0].get("ingredient").get("id") == 1, "Некорректный id ингридиента"
    assert recipe.get("ingredients")[0].get("count") == 2, "Некорректное количество"
    assert recipe.get("ingredients")[0].get("measure").get("id") == 1, "Некорректный id меры"
    assert recipe.get("tags")[0].get("id") == 1, "Некорректный id тэга"
    assert recipe == RECIPE_SAMPLE, "Некорректно выдан рецепт"

