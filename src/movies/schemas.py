import datetime

from pydantic import BaseModel


class GenrePostDTO(BaseModel):
    name: str


class GenreDTO(BaseModel):
    id: int
    name: str


class ActorPostDTO(BaseModel):
    name: str


class ActorDTO(BaseModel):
    id: int
    name: str


class MoviePostDTO(BaseModel):
    tmdb_id: int
    imdb_id: str
    kinopoisk_id: int
    localized_title: str
    original_title: str
    original_language: str
    overview: str
    release_date: datetime.date

    genres: list[int]
    actors: list[int]


class MovieDTO(BaseModel):
    id: int
    tmdb_id: int
    imdb_id: str
    kinopoisk_id: int
    localized_title: str
    original_title: str
    original_language: str
    overview: str
    release_date: datetime.date

    genres: list[GenreDTO]
    actors: list[ActorDTO]
