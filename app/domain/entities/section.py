from typing import List

from pydantic import Field

from .base_entity import BaseEntity
from .question import QuestionEntity


class SectionEntity(BaseEntity):
    title: str
    description: str | None = None
    questions: List[QuestionEntity] = Field(default_factory=list)
