from typing import Dict, Type

from .base import Command, CommandBus, CommandHandler


class SimpleCommandBus(CommandBus):
    """Simple implementation of command bus that routes commands to handlers."""

    def __init__(self):
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register_handler(self, command_type: Type[Command], handler: CommandHandler):
        """Register a handler for a specific command type."""
        self._handlers[command_type] = handler

    async def execute(self, command: Command):
        """Execute a command by routing it to the appropriate handler."""
        command_type = type(command)

        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for command type: {command_type}")

        handler = self._handlers[command_type]
        return await handler.handle(command)
