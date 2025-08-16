from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Command(ABC):
    """Base interface for all commands."""

    pass


class CommandHandler(ABC, Generic[T]):
    """Base interface for command handlers."""

    @abstractmethod
    async def handle(self, command: Command) -> T:
        """Handle the command and return the result."""
        pass


class CommandBus(ABC):
    """Interface for the command bus that routes commands to handlers."""

    @abstractmethod
    async def execute(self, command: Command):
        """Execute a command and return the result."""
        pass
