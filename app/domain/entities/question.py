from typing import List

from app.domain.value_objects.question_options import QuestionOption
from app.domain.value_objects.question_type import QuestionType

from .base_entity import BaseEntity


class QuestionEntity(BaseEntity):
    text: str
    type: QuestionType
    options: List[QuestionOption] | None = None
    is_required: bool = True
