import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class APICreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    version: str = Field(min_length=1, max_length=50)
    specification: dict[str, Any]


class APIResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    version: str
    specification: dict[str, Any]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }