from sqlalchemy import Column, Integer, String, Boolean, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from src.models.mixins.mixins import TableMixin
from src.db.pg.settings import Base


class Measure(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    measure = Column(String(length=20), nullable=False, unique=True)


class IngredientType(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    type = Column(String(length=20), nullable=False, unique=True)


class Ingredient(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20), nullable=False, unique=True)


class Tag(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    tag = Column(String(length=20), nullable=False, unique=True)

    # RecipeType = relationship("RecipeTag", back_populates="Tag")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='Tag_id'),
        {'extend_existing': True},
    )


class Recipe(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), nullable=False)
    description = Column(String, nullable=False)
    execute_time = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User")  # , back_populates="Recipe")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='Recipe_id'),
        {'extend_existing': True},
    )


class IngredientCount(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
    count = Column(Integer, nullable=True, default=0)
    measure_id = Column(Integer, ForeignKey("measure.id"))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    recipes = relationship("Recipe")  # , back_populates="IngredientCount")
    measures = relationship("Measure")  # , back_populates="IngredientCount")
    ingredients = relationship("Ingredient")  # , back_populates="IngredientCount")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='IngredientCount_id'),
        {'extend_existing': True},
    )


class RecipeType(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))

    recipe = relationship("Recipe")  # , back_populates="RecipeType")
    tag = relationship("Tag")  # , back_populates="RecipeType")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='RecipeType_id'),
        {'extend_existing': True},
    )


class RecipeFile(TableMixin, Base):
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    filename = Column(String(length=40), nullable=False)
    is_preview = Column(Boolean, default=None)

    recipe = relationship("Recipe")  # , back_populates="RecipeFile")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='RecipeFile_id'),
        {'extend_existing': True},
    )
