from .property import HomeService, RoomService
from .elements import ElementService
from ..models.property import Home, Room
from ..models.elements import Element
from ..utils.logging import logger

class DemoService:
    """Service for creating demo data."""
    
    def __init__(self):
        self.home_service = HomeService()
        self.room_service = RoomService()
        self.element_service = ElementService()
    
    def create_demo_home(self) -> Home:
        """Create a demo home with rooms and elements."""
        try:
            # Create home
            home = self.home_service.create(Home(
                name="Demo Home",
                address="145 Testing Way"
            ))
            logger.info(f"Created demo home: {home.name}")
            
            # Create rooms
            kitchen = self.room_service.create(Room(
                name="Kitchen",
                level=1,
                home_id=home.id
            ))
            mechanical = self.room_service.create(Room(
                name="Mechanical Closet",
                level=1,
                home_id=home.id
            ))
            bathroom = self.room_service.create(Room(
                name="Bathroom",
                level=1,
                home_id=home.id
            ))
            logger.info(f"Created demo rooms in {home.name}")
            
            # Create elements
            self.element_service.create(Element(
                name="Fridge",
                equip_type="refrigerator",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Stove",
                equip_type="stove",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Dishwasher",
                equip_type="dishwasher",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Water Heater",
                equip_type="water heater - tank",
                room_id=mechanical.id
            ))
            self.element_service.create(Element(
                name="Heat Pump",
                equip_type="heat pump - ducted",
                room_id=mechanical.id
            ))
            logger.info(f"Created demo elements in {home.name}")
            
            return home
            
        except Exception as e:
            logger.error(f"Error creating demo home: {e}")
            raise 