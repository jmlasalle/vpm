from .property import HomeService, RoomService
from .elements import ElementService
from ..models.property import Home, Room
from ..models.elements import Element

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
            
            # Create elements
            self.element_service.create(Element(
                name="Fridge",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Stove",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Dishwasher",
                room_id=kitchen.id
            ))
            self.element_service.create(Element(
                name="Water Heater",
                room_id=mechanical.id
            ))
            self.element_service.create(Element(
                name="Heat Pump",
                room_id=mechanical.id
            ))
            
            return home
            
        except Exception as e:
            raise 