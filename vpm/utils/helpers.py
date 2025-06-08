from datetime import datetime, timezone
from typing import Any, Dict, Optional
from decimal import Decimal
import json
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY
from ..models.picklist import *

def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)

def format_decimal(value: Optional[Decimal], places: int = 2) -> str:
    """Format decimal value with specified number of decimal places."""
    if value is None:
        return ""
    return f"{value:.{places}f}"

def parse_decimal(value: str) -> Optional[Decimal]:
    """Parse string to Decimal, return None if invalid."""
    try:
        return Decimal(value)
    except (ValueError, TypeError):
        return None

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, TaskType):
        return obj.value
    if isinstance(obj, ElementType):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")

def to_dict(obj: Any) -> Dict:
    """Convert object to dictionary, handling special types."""
    def _serialize(obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        if hasattr(obj, "__dict__"):
            return {k: _serialize(v) for k, v in obj.__dict__.items()}
        return obj
    
    return _serialize(obj)

def json_serialize(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(to_dict(obj), indent=2)

def next_date(freq: str, interval: int, dt: datetime = None) -> datetime:
    """Calculate the next date based on frequency and interval."""
    if dt is None:
        dt = datetime.now()
        
    if freq.upper() not in ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]:
        raise ValueError(f'{freq.upper()} must be one of YEARLY, MONTHLY, WEEKLY, DAILY')
        
    return rrule(freq=eval(freq.upper()), interval=interval, dtstart=dt)[1] 

# validator functions
def validate_document_category(value: str) -> str:
    """Validate document category."""
    if value not in DocumentCategory:
        raise ValueError(f"Invalid document category: {value}")
    return value

def validate_task_category(value: str) -> str:
    """Validate task category."""
    if value not in TaskCategory:
        raise ValueError(f"Invalid task category: {value}")
    return value

def validate_task_status(value: str) -> str:
    """Validate task status."""
    if value not in TaskStatus:
        raise ValueError(f"Invalid task status: {value}")
    return value

def validate_currency(value: str) -> str:
    """Validate currency."""
    if value not in Currency:
        raise ValueError(f"Invalid currency: {value}")
    return value

def validate_interval_unit(value: str) -> str:
    """Validate interval unit."""
    if value not in IntervalUnit:
        raise ValueError(f"Invalid interval unit: {value}")
    return value