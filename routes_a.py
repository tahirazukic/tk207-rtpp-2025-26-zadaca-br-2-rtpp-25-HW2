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

