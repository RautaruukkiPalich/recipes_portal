from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from src.services.settings import JWT_SECRET, COOKIE_LIFETIME


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=COOKIE_LIFETIME)


cookie_transport = CookieTransport(
    cookie_name="cooking_jwt_token",
    cookie_max_age=COOKIE_LIFETIME,
)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
