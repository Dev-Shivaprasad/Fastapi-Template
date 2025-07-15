from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select
from models.hero_model import hero, addhero_create, addhero_update
from database.DB import Session, get_session
from utils.jwtdependencies import JWTBearer

HeroesRoutes = APIRouter(dependencies=[Depends(JWTBearer)])


# Create hero
@HeroesRoutes.post("/heroes/", response_model=hero, status_code=status.HTTP_201_CREATED)
def create_hero(hero_data: addhero_create, session: Session = Depends(get_session)):
    session.add(hero_data)
    session.commit()
    session.refresh(hero_data)
    return hero_data


# Get all heroes
@HeroesRoutes.get("/heroes/")
def get_all_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(hero)).all()
    if not heroes:
        raise HTTPException(status_code=404, detail="No heroes found")
    return heroes


# Get single hero
@HeroesRoutes.get("/heroes/{hero_id}", response_model=hero)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    Hero = session.get(hero, hero_id)
    if not Hero:
        raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")
    return Hero


# Update hero
@HeroesRoutes.put("/heroes/{hero_id}", response_model=hero)
def update_hero(
    hero_id: int, updates: addhero_update, session: Session = Depends(get_session)
):
    Hero = session.get_one(hero, hero_id)
    if not Hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID {hero_id} not found",
        )
    for key, value in updates.model_dump().items():
        setattr(Hero, key, value)

    session.commit()
    session.refresh(Hero)
    return Hero


# Delete hero
@HeroesRoutes.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    Hero = session.get(hero, hero_id)
    if not Hero:
        raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")

    session.delete(Hero)
    session.commit()
    return None
