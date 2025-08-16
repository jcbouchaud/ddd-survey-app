"""
Template API endpoints using the command pattern.

This demonstrates how to call services through commands instead of directly.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.helpers import handle_exceptions
from app.application.commands.factory import create_command_bus
from app.application.commands.template_commands import (
    AddQuestionCommand,
    AddSectionCommand,
    CreateTemplateCommand,
    EditQuestionCommand,
    PublishTemplateCommand,
)
from app.application.dtos.section import CreateSectionDTO
from app.application.dtos.template import CreateTemplateDTO
from app.domain.repositories.unit_of_work import AbstractUnitOfWork
from app.infrastructure.dependencies import get_uow

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create")
@handle_exceptions
async def create_template_endpoint(
    payload: CreateTemplateDTO,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        # Create command bus and execute command
        command_bus = create_command_bus(uow)
        command = CreateTemplateCommand(
            title=payload.title,
            description=payload.description,
        )
        template = await command_bus.execute(command)

    return JSONResponse(
        status_code=201,
        content={"message": "Template created", "template_id": str(template.id)},
        headers={"Location": f"/template/{template.id}"},
    )


@router.post("/{template_id}/publish")
@handle_exceptions
async def publish_template_endpoint(
    template_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        # Create command bus and execute command
        command_bus = create_command_bus(uow)
        command = PublishTemplateCommand(template_id=template_id)
        template = await command_bus.execute(command)

    return JSONResponse(
        status_code=200,
        content={"message": "Template published", "template_id": str(template.id)},
    )


@router.post("/{template_id}/sections")
@handle_exceptions
async def add_section_endpoint(
    template_id: UUID,
    data: CreateSectionDTO,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        # Create command bus and execute command
        command_bus = create_command_bus(uow)
        command = AddSectionCommand(
            template_id=template_id,
            title=data.title,
            description=data.description,
        )
        template = await command_bus.execute(command)

    return JSONResponse(
        status_code=201,
        content={"message": "Section added", "template_id": str(template.id)},
    )


@router.post("/{template_id}/sections/{section_id}/questions")
@handle_exceptions
async def add_question_endpoint(
    template_id: UUID,
    section_id: UUID,
    question_data: dict,  # You might want to create a proper DTO for this
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        # Create command bus and execute command
        command_bus = create_command_bus(uow)
        command = AddQuestionCommand(
            template_id=template_id,
            section_id=section_id,
            question_text=question_data["text"],
            question_type=question_data["type"],
            options=question_data.get("options"),
            required=question_data.get("required", False),
        )
        template = await command_bus.execute(command)

    return JSONResponse(
        status_code=201,
        content={"message": "Question added", "template_id": str(template.id)},
    )


@router.put("/{template_id}/sections/{section_id}/questions/{question_id}")
@handle_exceptions
async def edit_question_endpoint(
    template_id: UUID,
    section_id: UUID,
    question_id: UUID,
    question_data: dict,  # You might want to create a proper DTO for this
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        # Create command bus and execute command
        command_bus = create_command_bus(uow)
        command = EditQuestionCommand(
            template_id=template_id,
            section_id=section_id,
            question_id=question_id,
            question_text=question_data["text"],
            question_type=question_data["type"],
            options=question_data.get("options"),
            required=question_data.get("required", False),
        )
        template = await command_bus.execute(command)

    return JSONResponse(
        status_code=200,
        content={"message": "Question updated", "template_id": str(template.id)},
    )
