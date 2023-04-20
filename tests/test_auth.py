from tests.conftest import client


def test_register():

    data = {
              "email": "email",
              "password": "password",
              "is_active": True,
              "is_superuser": False,
              "is_verified": False,
              "nickname": "nickname",
              "first_name": "first_name",
              "last_name": "last_name"
            }

    response = client.post("/auth/register", json=data)

    assert response.status_code == 201, "Пользователь не добавлен"

