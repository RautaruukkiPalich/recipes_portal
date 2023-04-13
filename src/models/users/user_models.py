from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.pg.settings import Base
from src.models.mixins.mixins import TableMixin


class Role(TableMixin, Base):

    id = Column(Integer, primary_key=True)
    role = Column(String(50))

    userRole = relationship("UserRole")  # , back_populates="role")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='role_id'),
        {'extend_existing': True},
    )


# class User(TableMixin, Base):
#
#     id = Column(Integer, primary_key=True)
#     nickname = Column(String(50), default="")
#     first_name = Column(String(50), default="")
#     last_name = Column(String(50), default="")
#     email = Column(String(length=320), unique=True, index=True, nullable=False)
#     hashed_password = Column(String(length=1024), nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_deleted = Column(Boolean, default=False, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#
#     userRole = relationship("UserRole")  # , back_populates="user")
#     recipe = relationship(Recipe)  # , back_populates="user")
#
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='user_id'),
#         {'extend_existing': True},
#     )


class UserRole(TableMixin, Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

    user = relationship("User")  # , back_populates="userRole")
    role = relationship("Role")  # , back_populates="userRole")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='userRole_id'),
        {'extend_existing': True},
    )






