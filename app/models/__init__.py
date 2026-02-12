from app.db.base import Base

from .product import Product
from .baai_product import BAAIProduct
from .dragonkue_product import DragonkueBAAIProduct

from .lecture import Lecture
from .baai_lecture import BAAILecture
from .dragonkue_lecture import DragonkueBAAILecture

from .enums import DifficultyEnum