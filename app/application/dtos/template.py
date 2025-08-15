from pydantic import BaseModel, Field


class CreateTemplateDTO(BaseModel):
    title: str = Field(default="")
    description: str = Field(default="")
