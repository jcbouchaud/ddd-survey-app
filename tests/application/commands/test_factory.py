import pytest

from app.application.commands.factory import create_command_bus
from app.application.commands.template_commands import (
    CreateTemplateCommand,
    PublishTemplateCommand,
)
from app.infrastructure.persistence.unit_of_work_mock import UnitOfWorkMock


class TestCommandBusFactory:
    """Test cases for the command bus factory."""

    @pytest.fixture
    def uow(self):
        """Fixture for unit of work mock."""
        return UnitOfWorkMock()

    @pytest.mark.asyncio
    async def test_create_command_bus_has_all_handlers(self, uow):
        """Test that the factory creates a command bus with all handlers registered."""
        command_bus = create_command_bus(uow)

        # Test that all commands can be executed
        create_command = CreateTemplateCommand(
            title="Test Template", description="A test template"
        )
        async with uow:
            result = await command_bus.execute(create_command)
        assert result.title == "Test Template"

        publish_command = PublishTemplateCommand(template_id=result.id)
        # This will fail because the template has no questions
        async with uow:
            with pytest.raises(
                ValueError, match="Cannot publish an empty survey template"
            ):
                await command_bus.execute(publish_command)

    @pytest.mark.asyncio
    async def test_create_command_bus_handlers_are_configured(self, uow):
        """Test that all handlers are properly configured in the factory."""
        command_bus = create_command_bus(uow)

        # Test that CreateTemplateCommand handler is registered
        create_command = CreateTemplateCommand(title="Test")
        async with uow:
            result = await command_bus.execute(create_command)
        assert result.title == "Test"

        # Test that PublishTemplateCommand handler is registered
        publish_command = PublishTemplateCommand(template_id=result.id)
        # This will fail because the template has no questions
        async with uow:
            with pytest.raises(
                ValueError, match="Cannot publish an empty survey template"
            ):
                await command_bus.execute(publish_command)
