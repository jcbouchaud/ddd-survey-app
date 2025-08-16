"""
Example of how to use the command pattern in your API endpoints.

This demonstrates how to call your services through commands instead of directly.
"""

from uuid import UUID

from app.application.commands.factory import create_command_bus
from app.application.commands.template_commands import (
    AddQuestionCommand,
    AddSectionCommand,
    CreateTemplateCommand,
    EditQuestionCommand,
    PublishTemplateCommand,
)
from app.infrastructure.dependencies import get_unit_of_work


async def create_template_example():
    """Example of creating a template using commands."""
    uow = get_unit_of_work()
    command_bus = create_command_bus(uow)

    # Create a command
    command = CreateTemplateCommand(
        title="Customer Satisfaction Survey",
        description="Survey to measure customer satisfaction",
    )

    # Execute the command
    template = await command_bus.execute(command)
    return template


async def publish_template_example(template_id: UUID):
    """Example of publishing a template using commands."""
    uow = get_unit_of_work()
    command_bus = create_command_bus(uow)

    command = PublishTemplateCommand(template_id=template_id)
    template = await command_bus.execute(command)
    return template


async def add_section_example(template_id: UUID):
    """Example of adding a section using commands."""
    uow = get_unit_of_work()
    command_bus = create_command_bus(uow)

    command = AddSectionCommand(
        template_id=template_id,
        title="Product Quality",
        description="Questions about product quality",
    )

    template = await command_bus.execute(command)
    return template


async def add_question_example(template_id: UUID, section_id: UUID):
    """Example of adding a question using commands."""
    uow = get_unit_of_work()
    command_bus = create_command_bus(uow)

    command = AddQuestionCommand(
        template_id=template_id,
        section_id=section_id,
        question_text="How would you rate our product quality?",
        question_type="single_choice",
        options=["Excellent", "Good", "Average", "Poor", "Very Poor"],
        required=True,
    )

    template = await command_bus.execute(command)
    return template


async def edit_question_example(template_id: UUID, section_id: UUID, question_id: UUID):
    """Example of editing a question using commands."""
    uow = get_unit_of_work()
    command_bus = create_command_bus(uow)

    command = EditQuestionCommand(
        template_id=template_id,
        section_id=section_id,
        question_id=question_id,
        question_text="How would you rate our product quality on a scale of 1-5?",
        question_type="number",
        required=True,
    )

    template = await command_bus.execute(command)
    return template
