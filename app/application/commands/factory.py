from app.domain.repositories.unit_of_work import AbstractUnitOfWork

from .command_bus import SimpleCommandBus
from .handlers import (
    AddQuestionHandler,
    AddSectionHandler,
    CreateTemplateHandler,
    EditQuestionHandler,
    PublishTemplateHandler,
)
from .template_commands import (
    AddQuestionCommand,
    AddSectionCommand,
    CreateTemplateCommand,
    EditQuestionCommand,
    PublishTemplateCommand,
)


def create_command_bus(uow: AbstractUnitOfWork) -> SimpleCommandBus:
    """Factory function to create and configure a command bus with all handlers."""
    command_bus = SimpleCommandBus()

    # Register all command handlers
    command_bus.register_handler(CreateTemplateCommand, CreateTemplateHandler(uow))
    command_bus.register_handler(PublishTemplateCommand, PublishTemplateHandler(uow))
    command_bus.register_handler(AddSectionCommand, AddSectionHandler(uow))
    command_bus.register_handler(AddQuestionCommand, AddQuestionHandler(uow))
    command_bus.register_handler(EditQuestionCommand, EditQuestionHandler(uow))

    return command_bus
