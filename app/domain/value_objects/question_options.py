from pydantic import BaseModel


class QuestionOption(BaseModel):
    label: str
    value: str
    order: int

    class Config:
        frozen = True  # Makes this immutable
