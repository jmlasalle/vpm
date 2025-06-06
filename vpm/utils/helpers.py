from datetime import datetime, timezone
from typing import Any, Dict, Optional
from decimal import Decimal
import json
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY

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
    """Calculate the next date based on frequency and interval.
    
    Args:
        freq: Frequency ('YEARLY', 'MONTHLY', 'WEEKLY', 'DAILY')
        interval: Number of frequency units
        dt: Start date (defaults to current date)
    
    Returns:
        Next date based on frequency and interval
    """
    if dt is None:
        dt = datetime.now()
        
    if freq.upper() not in ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]:
        raise ValueError(f'{freq.upper()} must be one of YEARLY, MONTHLY, WEEKLY, DAILY')
        
    return rrule(freq=eval(freq.upper()), interval=interval, dtstart=dt)[1] 