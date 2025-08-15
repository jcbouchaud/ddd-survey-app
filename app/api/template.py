import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.helpers import handle_exceptions
from app.application.dtos.section import CreateSectionDTO
from app.application.dtos.template import CreateTemplateDTO
from app.application.services.template_service import (
    add_section,
    create_template,
    publish_template,
)
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
        template = await create_template(
            uow=uow,
            title=payload.title,
            description=payload.description,
        )

    return JSONResponse(
        status_code=201,
        content={"message": "Template created"},
        headers={"Location": f"/template/{template.id}"},
    )


@router.post("/{template_id}/publish")
@handle_exceptions
async def publish_template_endpoint(
    template_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        await publish_template(uow=uow, template_id=template_id)

    return JSONResponse(status_code=200, content={"message": "Template published"})


@router.post("/{template_id}/sections")
@handle_exceptions
async def add_section_endpoint(
    template_id: UUID,
    data: CreateSectionDTO,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Response:
    async with uow:
        await add_section(uow=uow, template_id=template_id, data=data)

    return JSONResponse(status_code=201, content={"message": "Section added"})
