from typing import List

from pydantic import BaseModel, Field


class CreateQuestionDTO(BaseModel):
    text: str = Field(..., description="Question text")
    type: str = Field(
        ...,
        description=(
            "Question type (single_choice, multiple_choice, text, number, "
            "date, time, datetime, boolean, dropdown)"
        ),
    )
    options: List[str] | None = Field(
        default=None, description="Options for choice questions"
    )
    required: bool = Field(default=True, description="Whether the question is required")


class UpdateQuestionDTO(BaseModel):
    text: str = Field(..., description="Question text")
    type: str = Field(
        ...,
        description=(
            "Question type (single_choice, multiple_choice, text, number, "
            "date, time, datetime, boolean, dropdown)"
        ),
    )
    options: List[str] | None = Field(
        default=None, description="Options for choice questions"
    )
    required: bool = Field(default=True, description="Whether the question is required")
