from fastapi import FastAPI, responses, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from models.hero_model import hero
from database.DB import Session, get_session
from sqlmodel import select
from authentication.auth import generate_jwt

app = FastAPI(title="Your app name")

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
# app.include_router(example.router, prefix="/api")


@app.get("/")
def root():
    responses.Response.set_cookie
    return {"message": "Welcome to the FastAPI Boilerplate"}


@app.post("/PostHeros/", response_model=hero)
def create_Hero(Hero: hero, session: Session = Depends(get_session)):
    session.add(Hero)
    session.commit()
    session.refresh(Hero)
    return Hero


@app.get("/GetAllHeros")
def get_Hero(session: Session = Depends(get_session)):
    return session.exec(statement=select(hero)).all()


@app.get("/GetSomeHeros/{id}")
def get_Some_Hero(id: int, session: Session = Depends(get_session)):
    daat = session.get_one(hero, id)
    if not daat:
        print(daat)
        return {
            "status": status.HTTP_204_NO_CONTENT,
            "content": f"hero did not found with id {id}",
        }
    print(daat)
    return daat


@app.get("/jwt")
async def sendjwt():
    # Retrive data from the DB and embed it with the specfiv attributs
    # It is better to create a Schema of the payload
    data = {"userid": 123456, "username": "shivaprasad", "role": ["Admin", "user"]}
    return await generate_jwt(payload=data)
