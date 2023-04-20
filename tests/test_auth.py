from httpx import AsyncClient


async def test_register(ac: AsyncClient):
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

    response = await ac.post("/auth/register", json=data)

    assert response.status_code == 201, "Пользователь не добавлен"


class JWT:
    def __init__(self, token=None):
        self.token = token

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token


jwt_token = JWT()


async def test_login(ac: AsyncClient):
    data = {
        "username": "email",
        "password": "password",
    }

    response = await ac.post("/auth/jwt/login",
                             data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"}
                             )

    assert response.status_code == 200, "Пользователь не залогининся"
    assert response.headers.get("set-cookie", None) is not None, "Не выданы куки"

    jwt_token.set_token(response.headers.get("set-cookie"))


async def test_logout(ac: AsyncClient):

    response = await ac.post("/auth/jwt/logout", headers={"Cookie": jwt_token.get_token()})

    assert response.status_code == 200, "Пользователь не был авторизован"

    jwt_token.set_token("")
    response = await ac.post("/auth/jwt/logout", headers={"Cookie": jwt_token.get_token()})

    assert response.status_code == 401, "Пользователь ещё авторизован"
