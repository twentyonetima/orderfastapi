from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.routes import router as users_router
from order.routes import router as orders_router
from database import engine, init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(engine)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(orders_router)
