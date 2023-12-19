import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base

metadata = Base.metadata

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())")),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class MovieGenre(Base):
    __tablename__ = "movie_genre"

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movie.id", ondelete="CASCADE"),
        primary_key=True,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.id", ondelete="CASCADE"),
        primary_key=True,
    )


class MovieActor(Base):
    __tablename__ = "movie_actor"

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movie.id", ondelete="CASCADE"),
        primary_key=True,
    )
    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actor.id", ondelete="CASCADE"),
        primary_key=True,
    )


class UserWatchlist(Base):
    __tablename__ = "user_watchlist"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movie.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[intpk]
    tmdb_id: Mapped[int]
    imdb_id: Mapped[str]
    kinopoisk_id: Mapped[int]
    localized_title: Mapped[str]
    original_title: Mapped[str]
    original_language: Mapped[str]
    overview: Mapped[str]
    release_date: Mapped[datetime.date]

    genres: Mapped[list["Genre"]] = relationship(
        back_populates="movies",
        secondary="movie_genre",
    )
    actors: Mapped[list["Actor"]] = relationship(
        back_populates="movies",
        secondary="movie_actor",
    )


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[intpk]
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(
        back_populates="genres",
        secondary="movie_genre",
    )


class Actor(Base):
    __tablename__ = "actor"

    id: Mapped[intpk]
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(
        back_populates="actors",
        secondary="movie_actor",
    )
