# Command Pattern Implementation

This module implements the Command pattern for calling services in a clean, decoupled way.

## Overview

The Command pattern provides several benefits:
- **Decoupling**: API layer doesn't need to know about service implementation details
- **Testability**: Commands can be easily mocked and tested in isolation
- **Extensibility**: Easy to add cross-cutting concerns like logging, validation, etc.
- **Consistency**: All service calls follow the same pattern

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   API Layer │───▶│   Command    │───▶│   Handler   │───▶│   Domain    │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
                          │                     │
                          ▼                     ▼
                   ┌──────────────┐    ┌─────────────┐
                   │ Command Bus  │    │ Repository  │
                   └──────────────┘    └─────────────┘
```

## Components

### 1. Commands (`template_commands.py`)
Commands encapsulate the parameters needed for a specific operation:

```python
class CreateTemplateCommand(Command, BaseModel):
    title: str
    description: str | None = None
```

### 2. Handlers (`handlers.py`)
Handlers contain the business logic directly:

```python
class CreateTemplateHandler(CommandHandler[TemplateAggregate]):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
    
    async def handle(self, command: CreateTemplateCommand) -> TemplateAggregate:
        new_template = await self.uow.template.create(
            TemplateAggregate(title=command.title, description=command.description)
        )
        await self.uow.commit()
        return new_template
```

### 3. Command Bus (`command_bus.py`)
The command bus routes commands to their appropriate handlers:

```python
class SimpleCommandBus(CommandBus):
    def __init__(self):
        self._handlers: Dict[Type[Command], CommandHandler] = {}
    
    def register_handler(self, command_type: Type[Command], handler: CommandHandler):
        self._handlers[command_type] = handler
    
    async def execute(self, command: Command):
        command_type = type(command)
        handler = self._handlers[command_type]
        return await handler.handle(command)
```

### 4. Factory (`factory.py`)
The factory creates and configures the command bus with all registered handlers:

```python
def create_command_bus(uow: AbstractUnitOfWork) -> SimpleCommandBus:
    command_bus = SimpleCommandBus()
    
    # Register all command handlers
    command_bus.register_handler(CreateTemplateCommand, CreateTemplateHandler(uow))
    command_bus.register_handler(PublishTemplateCommand, PublishTemplateHandler(uow))
    # ... more handlers
    
    return command_bus
```

## Usage

### In API Endpoints

Instead of calling services directly:

```python
# Old way
template = await create_template(uow=uow, title="Survey", description="Test")

# New way with commands (business logic in handlers)
command_bus = create_command_bus(uow)
command = CreateTemplateCommand(title="Survey", description="Test")
template = await command_bus.execute(command)

### Complete Example

```python
@router.post("/create")
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
    )
```

## Available Commands

### Template Commands
- `CreateTemplateCommand`: Create a new template
- `PublishTemplateCommand`: Publish a template
- `AddSectionCommand`: Add a section to a template
- `AddQuestionCommand`: Add a question to a section
- `EditQuestionCommand`: Edit a question in a section

## Benefits

1. **Separation of Concerns**: API layer focuses on HTTP, handlers contain business logic
2. **Testability**: Easy to unit test commands and handlers in isolation
3. **Maintainability**: Business logic is self-contained in handlers
4. **Consistency**: All operations follow the same command pattern
5. **Extensibility**: Easy to add middleware, validation, logging, etc.

## Future Enhancements

You can easily extend this pattern with:

1. **Command Validation**: Add validation decorators to commands
2. **Command Logging**: Add logging middleware to track all commands
3. **Command Authorization**: Add authorization checks to commands
4. **Command Events**: Emit events after command execution
5. **Command Queuing**: Queue commands for background processing

## Testing

Commands and handlers can be easily tested:

```python
async def test_create_template_command():
    uow = MockUnitOfWork()
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="Test", description="Test desc")
    
    result = await handler.handle(command)
    
    assert result.title == "Test"
    assert result.description == "Test desc"
```
