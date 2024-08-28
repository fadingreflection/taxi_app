"""Entrypoint configs."""
from fastapi import FastAPI

from db_management.db.database import Base, engine
from db_management.db_endpoints import trips, users
from predictor import predictor_endpoints

app = FastAPI()


app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(predictor_endpoints.router, prefix="/api/predictor",
                   tags=["Predictor"])


@app.on_event("startup")
def startup_db() -> None:
    """Startup database."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> str:
    """Read root."""
    return {"message": "Welcome to the Taxi App API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
