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

