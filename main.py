from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Resources
movies = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010
    },
    {
        "id": 2,
        "title": "Endgame",
        "director": "Anthony Russo, Joe Russo",
        "year": 2019
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "year": 2008
    }
]

class MovieCreate(BaseModel):
    title: str
    director: str
    year: int

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI!"
    }

@app.get("/movies")
def get_movies(min_year: int | None = None):

    result = movies

    if min_year is not None:
        result = [
            movie
            for movie in result
            if movie["year"] >= min_year
        ]

        return result

@app.get("/movies/{id}")
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie

    raise HTTPException (
        status_code=404,
        detail="Movie not found"
    )


@app.post("/movies", status_code=201)
def create_movie(movie: MovieCreate):

    new_movie = {
        "id": len(movies) + 1,
        "title": movie.title,
        "director": movie.director,
        "year": movie.year
    }

    movies.append(new_movie)
    return new_movie

@app.put("/movies/(id)")
def update_movie(id: int, movie: MovieCreate):

    for index, existing_movie in enumerate(movies):

        if existing_movie["id"] == id:

            updated_movie = {
                "id": id,
                "title": movie.title,
                "director": movie.director,
                "year": movie.year
            }

            movies[index] = updated_movie

            return updated_movie
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

@app.patch("/movies/{id}")
def patch_movie(id: int, movie_update: MovieUpdate):

    for movie in movies:

        if movie["id"] == id:

            updates = movie_update.model_dump(exclude_unset=True)

            movie.update(updates)

            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )

@app.delete("/movies/{id}", status_code=204)
def delete_movie(id: int):

    for index, movie in enumerate(movies):

        if movie["id"] == id:
            movies.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )