from copy import deepcopy

from httpx import AsyncClient


# TAGS
async def test_add_tag(ac: AsyncClient):
    data = {
        "tag": "custom_tag_name"
    }
    url = "/api/v1/recipes/tags/"

    response = await ac.post(url, json=data)
    assert response.status_code == 200


async def test_get_tags(ac: AsyncClient):
    url = "/api/v1/recipes/tags/"
    response = await ac.get(url, params=None)

    assert response.status_code == 200, "Тэги не поулчены"
    assert response.json()[0]["tag"] == "custom_tag_name", "Получен неправильный тэг"
    assert len(response.json()) == 1, "Получен НЕ один тэг"


async def test_del_tag(ac: AsyncClient):
    url = "/api/v1/recipes/tags/1"
    response = await ac.delete(url, params=None)

    assert response.status_code == 200, "Тэг не удалён"
    assert response.json().get("error") is None, "Ошибка в response"


async def test_patch_tag(ac: AsyncClient):
    url = "/api/v1/recipes/tags/1"
    response = await ac.patch(url, params=None)

    assert response.status_code == 200, "Тэг не восстановлен"
    assert response.json().get("error") is None, "Ошибка в response"


# MEASURES
async def test_add_measure(ac: AsyncClient):
    data = {
        "measure": "custom_measure_name"
    }
    url = "/api/v1/recipes/measures/"

    response = await ac.post(url, json=data)
    assert response.status_code == 200


async def test_get_measures(ac: AsyncClient):
    url = "/api/v1/recipes/measures/"
    response = await ac.get(url, params=None)

    assert response.status_code == 200, "Мера не поулчена"
    assert response.json()[0]["measure"] == "custom_measure_name", "Получена неправильная мера"
    assert len(response.json()) == 1, "Получена НЕ одна мера"


# INGREDIENTS
async def test_add_ingredients(ac: AsyncClient):
    data = {
        "name": "custom_ingredient_name"
    }
    url = "/api/v1/recipes/ingredients/"

    response = await ac.post(url, json=data)
    assert response.status_code == 200


async def test_get_ingredients(ac: AsyncClient):
    url = "/api/v1/recipes/ingredients/"
    response = await ac.get(url, params=None)

    assert response.status_code == 200, "Ингредиент не поулчен"
    assert response.json()[0]["name"] == "custom_ingredient_name", "Получен неправильный ингредиент"
    assert len(response.json()) == 1, "Получен НЕ один ингредиент"


# RECIPES
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

    url = "/api/v1/recipes/"
    response = await ac.post(url, json=data)

    assert response.status_code == 200
    assert response.json().get("error", False) is None


async def test_get_recipe(ac: AsyncClient):
    url = "/api/v1/recipes/1"
    response = await ac.get(url, params={"recipe_id": 1})
    recipe = response.json()

    assert response.status_code == 200, "Рецепт не получен"
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
