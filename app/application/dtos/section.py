from pydantic import BaseModel, Field


class CreateSectionDTO(BaseModel):
    title: str = Field(default="")
    description: str = Field(default="")
