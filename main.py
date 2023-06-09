import uvicorn
from fastapi import FastAPI

from database import SessionLocal, engine, Base

from routers import user as UserRouter

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Movie Tracker")
app.include_router(UserRouter.router, prefix="/user")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost",
                port=8000, reload=True, workers=3)
