from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from uvicorn import run
import os
from math import ceil
from utils.helperfunctions import is_development

# from utils.helperfunctions import IsDevelopment
from routes.todo_routes import TodoRoutes
from routes.auth_routes import AuthRoutes
from database.cachelayer.rediscache import rediscachelifecycle

security = HTTPBearer()
swaggerenabled = is_development()

version = "v1"
app = FastAPI(
    title="TODO",
    description="",
    version=version,
    docs_url=swaggerenabled,
    redoc_url=swaggerenabled,
    default_response_class=ORJSONResponse,
    lifespan=rediscachelifecycle,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Middleware
# app.add_middleware(logger)

# Rate Limiter
# init_rate_limiter(app)

# # Routes


@app.get("/")
def root():
    return {"message": "Welcome to the Fullstack FastAPI Boilerplate"}


app.include_router(AuthRoutes, prefix="/api", tags=["Authentication"])
app.include_router(TodoRoutes, prefix="/api", tags=["TODO"])

if __name__ == "__main__":
    run(app="main:app", host="0.0.0.0", port=8000, workers=ceil((os.cpu_count() or 10) / 2))
