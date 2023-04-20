import os

from dotenv import load_dotenv

load_dotenv()

origins = [
    "http://localhost:5500",
    "http://localhost:63343",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:63343",
]


DB_NAME = os.environ.get('DB_NAME', 'cooking_db')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'postgres')
DB_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # ?asyncpg_fallback=True"

JWT_SECRET = os.environ.get('JWT_SECRET', 'SECRET')
RESET_PASS_SECRET = os.environ.get('RESET_PASS_SECRET', 'SECRET')
VERIFICATION_SECRET = os.environ.get('VERIFICATION_SECRET', 'SECRET')
COOKIE_LIFETIME = os.environ.get('COOKIE_LIFETIME', 3600 * 24 * 7)  # week
ORIGINS = os.environ.get('ORIGINS', origins)



# Tests

DB_TEST_NAME = os.environ.get('DB_TEST_NAME', 'cooking_test_db')
DB_TEST_HOST = os.environ.get('DB_TEST_HOST', 'localhost')
DB_TEST_PORT = os.environ.get('DB_TEST_PORT', '5432')
DB_TEST_USER = os.environ.get('DB_TEST_USER', 'postgres')
DB_TEST_PASS = os.environ.get('DB_TEST_PASS', 'postgres')
DB_TEST_URI = f"postgresql+asyncpg://{DB_TEST_USER}:{DB_TEST_PASS}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}"
