from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime, timezone

class BaseModel(SQLModel):
    """Base model with common fields for all models."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: str = Field(default=None, nullable=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
        nullable=False,
    ) 