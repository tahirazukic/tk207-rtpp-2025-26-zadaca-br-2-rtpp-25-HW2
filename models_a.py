import datetime

from sqlmodel import SQLModel, Field
from typing import Optional

# TODO: Student A - Definiši svoj SQLModel entitet ovdje
# 
class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    release_year: int
    price: float= Field(default=0.0)
    is_available: bool = Field(default=True)  
    world_premiere: datetime.date  

class AlbumCreate(SQLModel):
    title: str
    artist: str
    release_year: int
    price: float = Field(default=0.0)
    is_available: bool = Field(default=True)  
    world_premiere: datetime.date

class AlbumUpdate(SQLModel):
    id: Optional[int] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    release_year: Optional[int] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    world_premiere: Optional[datetime.date] = None



 
