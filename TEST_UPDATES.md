# Test Updates for Handler-Based Architecture

## Overview

The test suite has been completely updated to work with the new handler-based architecture after removing the service layer. All tests now focus on testing the command handlers directly.

## What Changed

### 1. Removed Service Tests

**Deleted:** `tests/application/services/test_template_service.py`

The old service tests were testing functions like:
- `create_template()`
- `publish_template()`
- `add_section()`

### 2. Created New Handler Tests

**Created:** `tests/application/commands/test_template_handlers.py`

New comprehensive tests for all command handlers:
- `CreateTemplateHandler`
- `PublishTemplateHandler`
- `AddSectionHandler`
- `AddQuestionHandler`
- `EditQuestionHandler`

### 3. Created Command Bus Tests

**Created:** `tests/application/commands/test_command_bus.py`

Tests for the command bus functionality:
- Command execution
- Handler registration
- Error handling for unregistered commands

### 4. Created Factory Tests

**Created:** `tests/application/commands/test_factory.py`

Tests for the command bus factory:
- Factory creates command bus with all handlers
- Handlers are properly configured

## Test Structure

```
tests/
├── application/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── test_template_handlers.py    # Handler tests
│   │   ├── test_command_bus.py          # Command bus tests
│   │   └── test_factory.py              # Factory tests
│   └── services/                        # REMOVED
└── domain/
    └── aggregates/
        └── test_template_aggregate.py   # Domain tests (unchanged)
```

## Handler Test Coverage

### CreateTemplateHandler Tests
- ✅ Successful template creation
- ✅ Template creation without description
- ✅ Proper transaction management

### PublishTemplateHandler Tests
- ✅ Successful template publishing
- ✅ Template not found error
- ✅ Publishing empty template (should fail)
- ✅ Publishing already published template (should fail)

### AddSectionHandler Tests
- ✅ Successfully adding a section
- ✅ Template not found error
- ✅ Adding section to published template (should fail)

### AddQuestionHandler Tests
- ✅ Successfully adding a question with options
- ✅ Adding question without options
- ✅ Template not found error

### EditQuestionHandler Tests
- ✅ Successfully editing a question
- ✅ Template not found error

### Integration Tests
- ✅ Complete workflow: create → add section → add question → publish
- ✅ Error handling across all handlers
- ✅ Data consistency verification

## Key Differences from Service Tests

### Before (Service Tests)
```python
async def test_create_template_success(self, uow):
    async with uow:
        template = await create_template(uow, title, description)
    assert template.title == title
```

### After (Handler Tests)
```python
async def test_create_template_handler_success(self, uow):
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template", description="A new template description")
    async with uow:
        template = await handler.handle(command)
    assert template.title == "New Template"
```

## Benefits of New Test Structure

### ✅ **Direct Handler Testing**
Tests focus on the actual business logic in handlers, not intermediate service functions.

### ✅ **Command Pattern Testing**
Tests verify that commands are properly handled and executed.

### ✅ **Better Error Handling**
Tests use custom exceptions (`TemplateNotFoundError`) instead of generic ones.

### ✅ **Transaction Management**
Tests use proper context managers (`async with uow:`) to simulate real transaction lifecycle.

### ✅ **Integration Testing**
Tests cover complete workflows from command creation to execution.

## Running the Tests

```bash
# Run all command tests
pytest tests/application/commands/

# Run specific handler tests
pytest tests/application/commands/test_template_handlers.py

# Run command bus tests
pytest tests/application/commands/test_command_bus.py

# Run factory tests
pytest tests/application/commands/test_factory.py
```

## Test Fixtures

The new tests use the same fixtures as the old service tests:
- `uow`: UnitOfWorkMock instance
- `template_id`: UUID for template ID
- `section_id`: UUID for section ID
- `question_id`: UUID for question ID
- `sample_template`: Basic template fixture
- `draft_template`: Template with section and question
- `published_template`: Published template fixture

## Error Handling Tests

All handlers now properly test error scenarios:
- Template not found errors
- Domain rule violations (e.g., publishing empty templates)
- Business logic errors (e.g., editing published templates)

## Next Steps

1. **Run the new tests** to ensure they all pass
2. **Add more edge case tests** as needed
3. **Add performance tests** for command execution
4. **Add integration tests** with real repositories
5. **Add command validation tests** if validation is added

The test suite has been successfully updated to work with the new handler-based architecture!
