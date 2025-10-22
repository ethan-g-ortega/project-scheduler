from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import Base, engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.routes.customers import router as customers_router
from app.routes.projects import router as projects_router
from app.routes.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Tables now:", inspect(engine).get_table_names())  
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount routers with prefixes & tags
app.include_router(customers_router)
app.include_router(projects_router)
app.include_router(weather_router)








