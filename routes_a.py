from datetime import date

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models_a import Album, AlbumCreate, AlbumUpdate
from database import get_session

router = APIRouter(prefix="/Albumi", tags=["Resurs A"])

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
                is_available: Optional[bool] = None,
                world_premiere: Optional[date] = None
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

@router.get("/{album_id}", response_model=Album)
def read_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    return db_album   

@router.put("/{album_id}", response_model=Album)
def update_album(album_id: int, album_update: AlbumCreate, session: Session=Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    album_data = album_update.model_dump() 
    for key, value in album_data.items():
        setattr(db_album, key, value)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album

@router.patch("/{album_id}", response_model=Album)
def partial_update_album(album_id: int, album_update: AlbumUpdate, session: Session=Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    album_data = album_update.model_dump(exclude_unset=True) 
    for key, value in album_data.items():
        setattr(db_album, key, value)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    session.delete(db_album)
    session.commit()
    return None





   