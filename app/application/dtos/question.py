from pydantic import BaseModel, Field


class CreateQuestionDTO(BaseModel):
    title: str = Field(default="")
    description: str = Field(default="")
