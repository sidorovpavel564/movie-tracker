from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from src.database import Base
from src.movies.models import UserWatchlist

metadata = Base.metadata


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "user"

    watchlist: Mapped[list["Movie"]] = relationship(secondary="user_watchlist")
