# Tests

This directory contains comprehensive unit tests for the backend application.

## Structure

```
tests/
├── domain/
│   └── aggregates/
│       └── test_template_aggregate.py  # TemplateAggregate unit tests
├── application/
│   └── services/
│       └── test_template_service.py    # Template service unit tests
└── README.md
```

## Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
# Domain tests
python -m pytest tests/domain/aggregates/test_template_aggregate.py -v

# Application service tests
python -m pytest tests/application/services/test_template_service.py -v
```

### Run tests with coverage
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Test Coverage

### TemplateAggregate Tests (Domain Layer)

The `test_template_aggregate.py` file contains comprehensive unit tests for the `TemplateAggregate` domain aggregate, covering:

#### Template Creation
- ✅ Template creation with default values
- ✅ Template creation without ID
- ✅ Template with different question types

#### Template Publishing
- ✅ Successful publishing of valid templates
- ✅ Publishing already published templates (should fail)
- ✅ Publishing archived templates (should fail)
- ✅ Publishing empty templates (should fail)
- ✅ Publishing templates with empty sections (should fail)

#### Section Management
- ✅ Adding sections to draft templates
- ✅ Adding sections to published templates (should fail)
- ✅ Adding sections to archived templates (should fail)

#### Question Management
- ✅ Adding questions to sections
- ✅ Adding questions to non-existent sections (should fail)
- ✅ Adding questions to published templates (should fail)
- ✅ Adding questions to archived templates (should fail)
- ✅ Editing existing questions
- ✅ Editing non-existent questions (should fail)
- ✅ Editing questions in published templates (should fail)
- ✅ Editing questions in archived templates (should fail)

#### Template State Management
- ✅ Template status transitions
- ✅ Template immutability after publishing
- ✅ Complex templates with multiple sections and questions

#### Domain Rules Validation
- ✅ Draft templates can be edited
- ✅ Published templates cannot be edited
- ✅ Archived templates cannot be edited

## Test Fixtures

The tests use pytest fixtures to provide reusable test data:

- `template_id`, `section_id`, `question_id`: UUID fixtures for IDs
- `sample_template`: Basic template in DRAFT status
- `sample_section`: Sample section entity
- `sample_question`: Sample question entity
- `published_template`: Template that has been published
- `archived_template`: Template in archived status

## Domain-Driven Design

These tests follow Domain-Driven Design principles by:

1. **Testing domain rules**: Ensuring business rules are enforced (e.g., cannot edit published templates)
2. **Testing aggregate boundaries**: Verifying that the TemplateAggregate maintains consistency
3. **Testing domain invariants**: Ensuring that the aggregate remains in a valid state
4. **Testing domain events**: Verifying that state changes trigger appropriate updates

## Test Quality

- **Comprehensive coverage**: All public methods and edge cases are tested
- **Clear test names**: Each test method has a descriptive name explaining what it tests
- **Proper assertions**: Tests verify both positive and negative cases
- **Isolated tests**: Each test is independent and doesn't rely on other tests
- **Fast execution**: Tests run quickly and don't have external dependencies

### Template Service Tests (Application Layer)

The `test_template_service.py` file contains focused tests for service orchestration, avoiding redundancy with domain tests:

#### Service Orchestration Tests
- ✅ **Repository operations**: Tests that services correctly orchestrate repository calls
- ✅ **Domain method invocation**: Tests that services load aggregates and call domain methods
- ✅ **DTO handling**: Tests that services correctly handle DTOs and pass data to domain
- ✅ **Error propagation**: Tests that services propagate domain rule violations
- ✅ **Template not found**: Tests that services handle missing templates correctly

#### Service Integration Tests
- ✅ **Complete workflows**: Tests end-to-end service orchestration
- ✅ **Concurrent operations**: Tests service behavior with multiple operations
- ✅ **Data consistency**: Tests that services maintain consistency across operations
- ✅ **Boundary conditions**: Tests service handling of edge cases

#### Clean Separation of Concerns
- **Domain tests** → "If I call this method with X, does it obey the business rule?"
- **Service tests** → "When I trigger this use case, does it load the right aggregate and call the right domain method?"

#### Service Layer Characteristics
- **Orchestration focus**: Tests verify service orchestration, not domain rules
- **Repository abstraction**: Tests use mock repositories to isolate service logic
- **Error propagation**: Tests verify that domain exceptions are properly propagated
- **No redundancy**: Services don't re-test domain rules, only ensure they're invoked correctly
