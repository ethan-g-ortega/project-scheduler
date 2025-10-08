from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import Base, engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.routes.customers import router as customers_router
from app.routes.projects import router as projects_router
from app.routes.weather import router as weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Tables now:", inspect(engine).get_table_names())  # should show ['customers', 'projects']
    yield

app = FastAPI(lifespan=lifespan)

# Mount routers with prefixes & tags
app.include_router(customers_router)
app.include_router(projects_router)
app.include_router(weather_router)







