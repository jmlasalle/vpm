from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from ..database import engine
from ..models.property import Home, Room
from .base import BaseService

class HomeService(BaseService[Home]):
    """Service for managing homes."""
    
    def __init__(self):
        super().__init__(Home)
    
    def get_rooms(self, home_id: UUID) -> List[Room]:
        """Get all rooms in a home."""
        with Session(engine) as session:
            return session.exec(
                select(Room).where(Room.home_id == home_id)
            ).all()

class RoomService(BaseService[Room]):
    """Service for managing rooms."""
    
    def __init__(self):
        super().__init__(Room)
    
    def get_by_level(self, level: int) -> List[Room]:
        """Get all rooms on a specific level."""
        with Session(engine) as session:
            return session.exec(
                select(Room).where(Room.level == level)
            ).all() 