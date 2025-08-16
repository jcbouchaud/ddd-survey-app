# Context Manager Updates for Tests

## Overview

All tests have been updated to use proper context managers (`async with uow:`) to simulate the real transaction lifecycle. This ensures that tests accurately reflect how the handlers will be used in production.

## What Changed

### Before: Direct Handler Calls
```python
async def test_create_template_handler_success(self, uow):
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template")
    template = await handler.handle(command)  # Direct call without context
    assert template.title == "New Template"
```

### After: Context Manager Usage
```python
async def test_create_template_handler_success(self, uow):
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template")
    async with uow:  # Proper transaction context
        template = await handler.handle(command)
    assert template.title == "New Template"
```

## Updated Test Files

### 1. Handler Tests (`test_template_handlers.py`)
All handler tests now use context managers:
- ✅ `test_create_template_handler_success`
- ✅ `test_create_template_handler_without_description`
- ✅ `test_publish_template_handler_success`
- ✅ `test_publish_template_handler_not_found`
- ✅ `test_publish_empty_template_should_fail`
- ✅ `test_publish_already_published_template_should_fail`
- ✅ `test_add_section_handler_success`
- ✅ `test_add_section_handler_template_not_found`
- ✅ `test_add_section_to_published_template_should_fail`
- ✅ `test_add_question_handler_success`
- ✅ `test_add_question_handler_template_not_found`
- ✅ `test_add_question_handler_without_options`
- ✅ `test_edit_question_handler_success`
- ✅ `test_edit_question_handler_template_not_found`
- ✅ `test_handler_integration_workflow`
- ✅ `test_handler_error_handling`
- ✅ `test_handler_data_consistency`

### 2. Command Bus Tests (`test_command_bus.py`)
Command bus tests now use context managers:
- ✅ `test_command_bus_execute_success`
- ✅ `test_command_bus_unregistered_command`
- ✅ `test_command_bus_register_handler`

### 3. Factory Tests (`test_factory.py`)
Factory tests now use context managers:
- ✅ `test_create_command_bus_has_all_handlers`
- ✅ `test_create_command_bus_handlers_are_configured`

## Benefits of Context Manager Usage

### ✅ **Realistic Transaction Simulation**
Tests now properly simulate the transaction lifecycle that occurs in production.

### ✅ **Proper Error Handling**
Context managers ensure that exceptions are handled correctly within the transaction scope.

### ✅ **Consistent with Production Code**
Tests mirror how the handlers are actually used in the API endpoints.

### ✅ **Better Test Isolation**
Each test operates within its own transaction context, preventing interference.

### ✅ **Accurate Mock Behavior**
The mock unit of work can properly simulate transaction behavior.

## Context Manager Patterns

### Success Cases
```python
async with uow:
    template = await handler.handle(command)
assert template.title == "Expected Title"
```

### Error Cases
```python
async with uow:
    with pytest.raises(TemplateNotFoundError):
        await handler.handle(command)
```

### Integration Workflows
```python
# Step 1: Create template
async with uow:
    template = await create_handler.handle(create_command)

# Step 2: Add section
async with uow:
    template = await add_section_handler.handle(add_section_command)

# Step 3: Publish template
async with uow:
    template = await publish_handler.handle(publish_command)
```

## Transaction Lifecycle in Tests

1. **Context Entry**: `async with uow:` begins the transaction
2. **Handler Execution**: Handler performs business logic within transaction
3. **Commit**: Handler calls `await uow.commit()` to persist changes
4. **Context Exit**: Transaction is completed when context exits
5. **Assertions**: Verify the results after transaction completion

## Mock Unit of Work Behavior

The `UnitOfWorkMock` properly simulates:
- Transaction state management
- Commit tracking (`uow._committed`)
- Repository access within transaction context
- Proper cleanup on context exit

## Running Updated Tests

```bash
# Run all command tests with context managers
pytest tests/application/commands/

# Run specific test files
pytest tests/application/commands/test_template_handlers.py
pytest tests/application/commands/test_command_bus.py
pytest tests/application/commands/test_factory.py

# Run with verbose output to see context manager usage
pytest tests/application/commands/ -v
```

## Verification

All tests now properly:
- ✅ Use `async with uow:` context managers
- ✅ Handle both success and error cases within transactions
- ✅ Maintain proper transaction isolation
- ✅ Reflect real-world usage patterns
- ✅ Provide accurate test coverage

The test suite now accurately simulates the production transaction lifecycle!
