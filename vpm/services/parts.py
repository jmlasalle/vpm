from typing import Optional
from sqlmodel import Session, select
from ..models.parts import Part, PartType
from ..database.config import engine
from ..utils.logging import logger

class PartService:
    """Service for managing parts in the database."""
    
    def add_part(
        self,
        name: str,
        type: PartType,
        description: str,
        manufacturer: Optional[str] = None,
        model_number: Optional[str] = None,
        serial_number: Optional[str] = None
    ) -> Part:
        """Add a new part to the database.
        
        Args:
            name: Name of the part
            type: Type of the part
            description: Description of the part
            manufacturer: Optional manufacturer name
            model_number: Optional model number
            serial_number: Optional serial number
            
        Returns:
            The created Part instance
            
        Raises:
            ValueError: If a part with the same name already exists
        """
        with Session(engine) as session:
            # Check if part with same name exists
            existing = session.exec(
                select(Part).where(Part.name == name)
            ).first()
            
            if existing:
                raise ValueError(f"Part with name '{name}' already exists")
            
            # Create new part
            part = Part(
                name=name,
                type=type,
                description=description,
                manufacturer=manufacturer,
                model_number=model_number,
                serial_number=serial_number
            )
            
            session.add(part)
            session.commit()
            session.refresh(part)
            logger.info(f"Added new part: {name}")
            return part
    
    def get_part(self, name: str) -> Part:
        """Get a part by name.
        
        Args:
            name: Name of the part to retrieve
            
        Returns:
            The Part instance
            
        Raises:
            ValueError: If no part with the given name exists
        """
        with Session(engine) as session:
            part = session.exec(
                select(Part).where(Part.name == name)
            ).first()
            
            if not part:
                raise ValueError(f"No part found with name '{name}'")
            
            return part
    
    def update_part(self, part_id: str, **kwargs) -> Part:
        """Update a part's information.
        
        Args:
            part_id: ID of the part to update
            **kwargs: Fields to update and their new values
            
        Returns:
            The updated Part instance
            
        Raises:
            ValueError: If no part with the given ID exists
        """
        with Session(engine) as session:
            part = session.get(Part, part_id)
            
            if not part:
                raise ValueError(f"No part found with ID '{part_id}'")
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(part, key):
                    setattr(part, key, value)
            
            session.add(part)
            session.commit()
            session.refresh(part)
            logger.info(f"Updated part: {part.name}")
            return part
    
    def delete_part(self, part_id: str) -> None:
        """Delete a part.
        
        Args:
            part_id: ID of the part to delete
            
        Raises:
            ValueError: If no part with the given ID exists
        """
        with Session(engine) as session:
            part = session.get(Part, part_id)
            
            if not part:
                raise ValueError(f"No part found with ID '{part_id}'")
            
            session.delete(part)
            session.commit()
            logger.info(f"Deleted part: {part.name}") 