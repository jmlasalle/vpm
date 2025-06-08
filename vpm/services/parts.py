from typing import Optional
from sqlmodel import Session, select
from ..models.parts import Part, PartType
from ..database.config import engine
from .base import BaseService

class PartService(BaseService[Part]):
    """Service for managing parts in the database."""
    def __init__(self):
        super().__init__(Part)