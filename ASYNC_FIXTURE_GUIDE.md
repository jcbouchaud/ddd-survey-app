# Async Fixture with Context Manager Guide

## Overview

When working with async code and context managers in pytest, you need to properly set up async fixtures that can yield context managers. Here are the different approaches and best practices.

## Option 1: Async Fixture with Context Manager (Recommended)

This is the approach you're currently using, which is the most straightforward:

```python
@pytest.fixture
async def uow(self):
    """Fixture for unit of work mock."""
    uow = UnitOfWorkMock()
    async with uow:
        yield uow
```

### How it works:
1. Creates the unit of work
2. Enters the context manager (`async with uow:`)
3. Yields the uow to the test
4. When the test completes, exits the context manager
5. The context manager handles cleanup automatically

### Usage in tests:
```python
@pytest.mark.asyncio
async def test_create_template_handler_success(self, uow):
    """Test successful template creation."""
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template")
    
    # The uow is already in a context manager from the fixture
    template = await handler.handle(command)
    
    assert template.title == "New Template"
    assert uow._committed is True
```

## Option 2: Async Fixture with Manual Context Management

If you need more control over the context manager:

```python
@pytest.fixture
async def uow(self):
    """Fixture for unit of work mock."""
    uow = UnitOfWorkMock()
    yield uow
    # Manual cleanup if needed
    await uow.rollback()  # if rollback method exists
```

### Usage in tests:
```python
@pytest.mark.asyncio
async def test_create_template_handler_success(self, uow):
    """Test successful template creation."""
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template")
    
    async with uow:  # Manual context management in test
        template = await handler.handle(command)
    
    assert template.title == "New Template"
    assert uow._committed is True
```

## Option 3: Async Fixture with Factory Pattern

For more complex scenarios where you need different uow configurations:

```python
@pytest.fixture
async def uow_factory(self):
    """Factory fixture for creating unit of work instances."""
    def create_uow():
        return UnitOfWorkMock()
    
    yield create_uow

@pytest.fixture
async def uow(self, uow_factory):
    """Fixture for unit of work mock."""
    uow = uow_factory()
    async with uow:
        yield uow
```

## Option 4: Async Fixture with Dependency Injection

For testing different uow implementations:

```python
@pytest.fixture
async def uow(self, uow_type="mock"):
    """Fixture for unit of work with configurable type."""
    if uow_type == "mock":
        uow = UnitOfWorkMock()
    elif uow_type == "real":
        uow = RealUnitOfWork()  # if you have a real implementation
    
    async with uow:
        yield uow
```

## Best Practices

### 1. Always Use Context Managers
```python
# ✅ Good - Context manager in fixture
@pytest.fixture
async def uow(self):
    uow = UnitOfWorkMock()
    async with uow:
        yield uow

# ❌ Avoid - No context manager
@pytest.fixture
async def uow(self):
    uow = UnitOfWorkMock()
    yield uow  # No transaction lifecycle
```

### 2. Handle Exceptions Properly
```python
@pytest.fixture
async def uow(self):
    uow = UnitOfWorkMock()
    try:
        async with uow:
            yield uow
    except Exception:
        await uow.rollback()  # if available
        raise
```

### 3. Use Type Hints
```python
from app.domain.repositories.unit_of_work import AbstractUnitOfWork

@pytest.fixture
async def uow(self) -> AbstractUnitOfWork:
    """Fixture for unit of work mock."""
    uow = UnitOfWorkMock()
    async with uow:
        yield uow
```

### 4. Clean Up Resources
```python
@pytest.fixture
async def uow(self):
    uow = UnitOfWorkMock()
    async with uow:
        yield uow
    # Context manager automatically handles cleanup
    # No manual cleanup needed
```

## Current Implementation Analysis

Your current setup is correct:

```python
@pytest.fixture
async def uow(self):
    """Fixture for unit of work mock."""
    uow = UnitOfWorkMock()
    async with uow:
        yield uow
```

### Benefits:
- ✅ Each test gets a fresh uow instance
- ✅ Proper transaction lifecycle simulation
- ✅ Automatic cleanup via context manager
- ✅ Consistent with production usage

### Test Usage:
```python
@pytest.mark.asyncio
async def test_create_template_handler_success(self, uow):
    handler = CreateTemplateHandler(uow)
    command = CreateTemplateCommand(title="New Template")
    
    # uow is already in context manager from fixture
    template = await handler.handle(command)
    
    assert template.title == "New Template"
    assert uow._committed is True
```

## Troubleshooting

### Issue: "yield" not allowed in async function
**Solution:** Use `async def` with `yield` (Python 3.6+)

### Issue: Context manager not working
**Solution:** Ensure your UnitOfWorkMock implements `__aenter__` and `__aexit__`

### Issue: Tests not isolated
**Solution:** Each test gets a fresh uow instance from the fixture

### Issue: Commit not being tracked
**Solution:** Ensure your mock properly tracks `_committed` state

## Example UnitOfWorkMock Implementation

```python
class UnitOfWorkMock:
    def __init__(self):
        self._committed = False
        self.template = TemplateRepositoryMock()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Rollback on exception
            self._committed = False
        # Cleanup
    
    async def commit(self):
        self._committed = True
```

## Summary

Your current approach is the recommended pattern:

1. **Async fixture** with `async def`
2. **Context manager** with `async with uow:`
3. **Yield** the uow instance
4. **Automatic cleanup** via context manager exit

This provides the best balance of simplicity, correctness, and maintainability for testing async command handlers.
