from typing import List

import sqlalchemy.exc
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.database import get_async_session
from src.movies.models import Actor
from src.movies.models import Genre
from src.movies.models import Movie
from src.movies.schemas import ActorDTO
from src.movies.schemas import ActorPostDTO
from src.movies.schemas import GenrePostDTO
from src.movies.schemas import MovieDTO
from src.movies.schemas import MoviePostDTO
from src.movies.schemas import GenreDTO

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.post("/add-genre", response_model=GenreDTO)
async def add_genre(genre: GenrePostDTO,
                    session: AsyncSession = Depends(get_async_session)):
    query = select(Genre).filter_by(name=genre.name)
    result = await session.execute(query)
    result_list = result.scalars().all()
    if not result_list:
        stmt = (
            insert(Genre)
            .values(name=genre.name)
        )
        await session.execute(stmt)
        await session.commit()
        query = (
            select(Genre).filter_by(name=genre.name)
        )
        result = await session.execute(query)
        result_orm = result.scalar_one()
        result_dto = GenreDTO.model_validate(obj=result_orm,
                                             from_attributes=True)
        return result_dto
    else:
        result_list_dto = [GenreDTO.model_validate(row, from_attributes=True)
                           for row in result_list]
        return {"message": f"Genre '{genre.name}' already in table",
                "Genre": result_list_dto}


@router.post("/add-actor", response_model=ActorDTO)
async def add_actor(actor: ActorPostDTO,
                    session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Actor)
        .filter_by(name=actor.name)
    )
    result = await session.execute(query)
    result_list = result.scalars().all()
    if not result_list:
        stmt = (
            insert(Actor)
            .values(name=actor.name)
        )
        await session.execute(stmt)
        await session.commit()
        query = (
            select(Actor).filter_by(name=actor.name)
        )
        result = await session.execute(query)
        result_orm = result.scalar_one()
        result_dto = ActorDTO.model_validate(obj=result_orm,
                                             from_attributes=True)
        return result_dto
    else:
        result_list_dto = [ActorDTO.model_validate(row, from_attributes=True)
                           for row in result_list]
        return {"message": f"Genre '{actor.name}' already in table",
                "Genre": result_list_dto}


@router.post("/add-movie", response_model=MovieDTO)
async def add_movie(movie_data: MoviePostDTO,
                    session: AsyncSession = Depends(get_async_session)):
    movie1 = Movie(**movie_data.model_dump(exclude={"genres", "actors"}))
    genres_list = (await session.execute(
        select(Genre)
        .where(Genre.id.in_(movie_data.genres))
    )).scalars().all()
    movie1.genres = genres_list
    actors_list = (await session.execute(
        select(Actor)
        .where(Actor.id.in_(movie_data.actors))
    )).scalars().all()
    movie1.actors = actors_list
    session.add(movie1)
    await session.commit()
    result_movie_dto = MovieDTO.model_validate(obj=movie1,
                                               from_attributes=True)
    return result_movie_dto


@router.get("/movie-details", response_model=MovieDTO)
async def get_movie_details(movie_id: int,
                            session: AsyncSession = Depends(
                                get_async_session)):
    try:
        query = (
            select(Movie)
            .filter_by(id=movie_id)
            .options(
                selectinload(Movie.genres),
                selectinload(Movie.actors)
            )
        )
        result = await session.execute(query)
        result_orm = result.scalar_one()
        result_dto = MovieDTO.model_validate(obj=result_orm,
                                             from_attributes=True)
        return result_dto
    except sqlalchemy.exc.NoResultFound:
        content = {"message": "No result found."}
        return JSONResponse(content=content,
                            status_code=status.HTTP_404_NOT_FOUND)


@router.get("/movie-genres", response_model=List[GenreDTO])
async def get_movie_genres(movie_id: int,
                           session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Movie)
        .filter_by(id=movie_id)
        .options(selectinload(Movie.genres))
    )
    result = await session.execute(query)
    movie = result.scalar_one()
    result_orm = movie.genres
    result_dto = [GenreDTO.model_validate(row, from_attributes=True) for row in
                  result_orm]
    return result_dto


@router.get("/movie-actors", response_model=List[ActorDTO])
async def get_movie_actors(movie_id: int,
                           session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Movie)
        .filter_by(id=movie_id)
        .options(
            selectinload(Movie.actors)
        )
    )
    result = await session.execute(query)
    movie = result.scalar_one()
    result_orm = movie.actors
    result_dto = [ActorDTO.model_validate(row, from_attributes=True) for row in
                  result_orm]
    return result_dto


@router.delete("/remove-movie")
async def remove_movie(movie_id: int,
                       session: AsyncSession = Depends(get_async_session)):
    stmt = (
        delete(Movie)
        .filter_by(id=movie_id)
        .options(
            selectinload(Movie.actors),
            selectinload(Movie.genres)
        )
        .returning(Movie)
    )
    result = await session.execute(stmt)
    result_orm = result.scalar_one()
    result_dto = MovieDTO.model_validate(obj=result_orm, from_attributes=True)
    await session.commit()
    return result_dto


@router.put("/update-movie")
async def update_movie(movie_id: int, movie_data: MoviePostDTO,
                       session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(Movie)
        .filter_by(id=movie_id)
        .values(**movie_data.model_dump(exclude={"genres", "actors"}))
        .options(
            selectinload(Movie.genres),
            selectinload(Movie.actors)
        )
    ).returning(Movie)
    result = await session.execute(stmt)
    movie1 = result.scalar_one()
    new_genres_list = (await session.execute(
        select(Genre)
        .where(Genre.id.in_(movie_data.genres))
    )).scalars().all()
    movie1.genres = new_genres_list
    new_actors_list = (await session.execute(
        select(Actor)
        .where(Actor.id.in_(movie_data.actors))
    )).scalars().all()
    movie1.actors = new_actors_list
    await session.commit()
    result_dto = MovieDTO.model_validate(obj=movie1,
                                         from_attributes=True)
    return result_dto
