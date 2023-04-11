from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from src.db.pg.settings import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), default="")
    first_name: Mapped[str] = mapped_column(String(50), default="")
    last_name: Mapped[str] = mapped_column(String(50), default="")
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_on = mapped_column(TIMESTAMP, default=datetime.now)
    updated_on = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    deleted_on = mapped_column(TIMESTAMP, default=None)
