import pytest

from app.application.commands.command_bus import SimpleCommandBus
from app.application.commands.handlers import CreateTemplateHandler
from app.application.commands.template_commands import CreateTemplateCommand
from app.infrastructure.persistence.unit_of_work_mock import UnitOfWorkMock


class TestCommandBus:
    """Test cases for the command bus."""

    @pytest.fixture
    def uow(self):
        """Fixture for unit of work mock."""
        return UnitOfWorkMock()

    @pytest.fixture
    def command_bus(self, uow):
        """Fixture for command bus with registered handlers."""
        bus = SimpleCommandBus()
        bus.register_handler(CreateTemplateCommand, CreateTemplateHandler(uow))
        return bus

    @pytest.mark.asyncio
    async def test_command_bus_execute_success(self, command_bus, uow):
        """Test successful command execution."""
        command = CreateTemplateCommand(
            title="Test Template", description="A test template"
        )

        async with uow:
            result = await command_bus.execute(command)

        assert result.title == "Test Template"
        assert result.description == "A test template"
        assert result.id is not None

    @pytest.mark.asyncio
    async def test_command_bus_unregistered_command(self, uow):
        """Test that unregistered commands raise an error."""
        bus = SimpleCommandBus()
        command = CreateTemplateCommand(
            title="Test Template", description="A test template"
        )

        async with uow:
            with pytest.raises(
                ValueError, match="No handler registered for command type"
            ):
                await bus.execute(command)

    @pytest.mark.asyncio
    async def test_command_bus_register_handler(self, uow):
        """Test registering a handler."""
        bus = SimpleCommandBus()
        handler = CreateTemplateHandler(uow)
        command = CreateTemplateCommand(
            title="Test Template", description="A test template"
        )

        # Should fail before registration
        async with uow:
            with pytest.raises(ValueError):
                await bus.execute(command)

        # Register handler
        bus.register_handler(CreateTemplateCommand, handler)

        # Should succeed after registration
        async with uow:
            result = await bus.execute(command)
        assert result.title == "Test Template"
