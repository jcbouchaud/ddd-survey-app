from app.domain.aggregates.template import TemplateAggregate
from app.domain.entities.question import QuestionEntity
from app.domain.entities.section import SectionEntity
from app.domain.exceptions.template import TemplateNotFoundError
from app.domain.repositories.unit_of_work import AbstractUnitOfWork
from app.domain.value_objects.question_options import QuestionOption
from app.domain.value_objects.question_type import QuestionType

from .base import CommandHandler
from .template_commands import (
    AddQuestionCommand,
    AddSectionCommand,
    CreateTemplateCommand,
    EditQuestionCommand,
    PublishTemplateCommand,
)


class CreateTemplateHandler(CommandHandler[TemplateAggregate]):
    """Handler for creating templates."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def handle(self, command: CreateTemplateCommand) -> TemplateAggregate:
        new_template = await self.uow.template.create(
            TemplateAggregate(title=command.title, description=command.description)
        )
        await self.uow.commit()
        return new_template


class PublishTemplateHandler(CommandHandler[TemplateAggregate]):
    """Handler for publishing templates."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def handle(self, command: PublishTemplateCommand) -> TemplateAggregate:
        template = await self.uow.template.get_by_id(command.template_id)
        if not template:
            raise TemplateNotFoundError(f"Template {command.template_id} not found")

        template.publish()
        await self.uow.template.update(template)
        await self.uow.commit()
        return template


class AddSectionHandler(CommandHandler[TemplateAggregate]):
    """Handler for adding sections to templates."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def handle(self, command: AddSectionCommand) -> TemplateAggregate:
        template = await self.uow.template.get_by_id(command.template_id)
        if not template:
            raise TemplateNotFoundError(f"Template {command.template_id} not found")

        section = SectionEntity(title=command.title, description=command.description)
        template.add_section(section)
        await self.uow.template.update(template)
        await self.uow.commit()
        return template


class AddQuestionHandler(CommandHandler[TemplateAggregate]):
    """Handler for adding questions to sections."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def handle(self, command: AddQuestionCommand) -> TemplateAggregate:
        template = await self.uow.template.get_by_id(command.template_id)
        if not template:
            raise TemplateNotFoundError(f"Template {command.template_id} not found")

        # Create question options if provided
        options = None
        if command.options:
            options = [
                QuestionOption(label=opt, value=opt, order=i)
                for i, opt in enumerate(command.options)
            ]

        question = QuestionEntity(
            text=command.question_text,
            type=QuestionType(command.question_type),
            options=options,
            is_required=command.required,
        )

        template.add_question(command.section_id, question)
        await self.uow.template.update(template)
        await self.uow.commit()

        return template


class EditQuestionHandler(CommandHandler[TemplateAggregate]):
    """Handler for editing questions in sections."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def handle(self, command: EditQuestionCommand) -> TemplateAggregate:
        template = await self.uow.template.get_by_id(command.template_id)
        if not template:
            raise TemplateNotFoundError(f"Template {command.template_id} not found")

        # Create question options if provided
        options = None
        if command.options:
            options = [
                QuestionOption(label=opt, value=opt, order=i)
                for i, opt in enumerate(command.options)
            ]

        question = QuestionEntity(
            id=command.question_id,
            text=command.question_text,
            type=QuestionType(command.question_type),
            options=options,
            is_required=command.required,
        )

        template.edit_question(command.section_id, command.question_id, question)
        await self.uow.template.update(template)
        await self.uow.commit()

        return template
