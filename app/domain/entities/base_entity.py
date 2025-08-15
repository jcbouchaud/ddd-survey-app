from uuid import UUID

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    id: UUID | None = Field(default=None)
