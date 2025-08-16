from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities.question import QuestionEntity
from app.domain.entities.section import SectionEntity
from app.domain.value_objects.template_status import TemplateStatus


class TemplateAggregate(BaseModel):
    id: UUID | None = Field(default=None)
    title: str
    description: str | None = None
    status: TemplateStatus = TemplateStatus.DRAFT
    sections: List[SectionEntity] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def publish(self):
        """Domain rule: Only publish if at least one question exists."""
        if self.status == TemplateStatus.PUBLISHED:
            raise ValueError("Template is already published.")

        if self.status == TemplateStatus.ARCHIVED:
            raise ValueError("Cannot publish an archived template.")

        if not any(section.questions for section in self.sections):
            raise ValueError("Cannot publish an empty survey template.")

        self.status = TemplateStatus.PUBLISHED
        self.updated_at = datetime.utcnow()

    def add_section(self, data: SectionEntity):
        self._can_edit()
        self.sections.append(data)
        self.updated_at = datetime.utcnow()

    def add_question(self, section_id: UUID, data: QuestionEntity):
        self._can_edit()
        section = next((s for s in self.sections if s.id == section_id), None)
        if not section:
            raise ValueError(f"Section {section_id} not found.")
        section.questions.append(data)
        self.updated_at = datetime.utcnow()

    def edit_question(self, section_id: UUID, question_id: UUID, data: QuestionEntity):
        self._can_edit()
        section = next((s for s in self.sections if s.id == section_id), None)
        if not section:
            raise ValueError(f"Section {section_id} not found.")

        question = next((q for q in section.questions if q.id == question_id), None)
        if not question:
            raise ValueError(f"Question {question_id} not found.")

        index = section.questions.index(question)
        section.questions[index] = data
        self.updated_at = datetime.utcnow()

    def _can_edit(self):
        if self.status == TemplateStatus.PUBLISHED:
            raise ValueError("Cannot edit a published template.")
        if self.status == TemplateStatus.ARCHIVED:
            raise ValueError("Cannot edit an archived template.")
