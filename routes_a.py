from datetime import datetime
from turtle import title
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models_a import Album, AlbumCreate, AlbumUpdate
from database import get_session

router = APIRouter(prefix="/resursi_a", tags=["Resurs A"])

@router.post("/", response_model=Album, status_code=status.HTTP_201_CREATED)
def create_album(album: AlbumCreate, session: Session = Depends(get_session)):
    new_db_album = Album.model_validate(album)
    session.add(new_db_album)
    session.commit()
    session.refresh(new_db_album)
    return new_db_album

@router.get("/", response_model=List[Album])
def read_albums(
                session=Depends(get_session),
                title: Optional[str] = None,
                artist: Optional[str] = None,
                release_year: Optional[int] = None,
                price: Optional[float] = None,
                is_available: Optional[bool] = None
                world_premiere: Optional[datetime.date] = None
):
query_params={
    "title": title,
    "artist": artist,
    "release_year": release_year,
    "price": price,
    "is_available": is_available,
    "world_premiere": world_premiere
}
    query = select(Album)
    for key, value in query_params.items():
        if value is not None:
            query = query.where(getattr(Album, key) == value)
    albums = session.exec(query).all()
    return albums



   