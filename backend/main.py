from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from utils.helperfunctions import IsDevelopment
from routes.heroes_routes import HeroesRoutes
from routes.auth_routes import AuthRoutes

security = HTTPBearer()

version = "v1"
app = FastAPI(title="TODO", description="", version=version)


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
app.include_router(HeroesRoutes, prefix="/api", tags=["Heros"])
