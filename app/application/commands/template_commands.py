from uuid import UUID

from pydantic import BaseModel

from .base import Command


class CreateTemplateCommand(Command, BaseModel):
    """Command to create a new template."""

    title: str
    description: str | None = None


class PublishTemplateCommand(Command, BaseModel):
    """Command to publish a template."""

    template_id: UUID


class AddSectionCommand(Command, BaseModel):
    """Command to add a section to a template."""

    template_id: UUID
    title: str
    description: str | None = None


class AddQuestionCommand(Command, BaseModel):
    """Command to add a question to a section."""

    template_id: UUID
    section_id: UUID
    question_text: str
    question_type: str
    options: list[str] | None = None
    required: bool = False


class EditQuestionCommand(Command, BaseModel):
    """Command to edit a question in a section."""

    template_id: UUID
    section_id: UUID
    question_id: UUID
    question_text: str
    question_type: str
    options: list[str] | None = None
    required: bool = False
