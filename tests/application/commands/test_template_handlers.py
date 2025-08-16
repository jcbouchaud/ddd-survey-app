from datetime import datetime
from uuid import uuid4

import pytest

from app.application.commands.handlers import (
    AddQuestionHandler,
    AddSectionHandler,
    CreateTemplateHandler,
    EditQuestionHandler,
    PublishTemplateHandler,
)
from app.application.commands.template_commands import (
    AddQuestionCommand,
    AddSectionCommand,
    CreateTemplateCommand,
    EditQuestionCommand,
    PublishTemplateCommand,
)
from app.domain.aggregates.template import TemplateAggregate
from app.domain.entities.section import SectionEntity
from app.domain.exceptions.template import TemplateNotFoundError
from app.domain.value_objects.template_status import TemplateStatus
from app.infrastructure.persistence.unit_of_work_mock import UnitOfWorkMock


class TestTemplateHandlers:
    """Test cases for template command handlers."""

    @pytest.fixture
    def uow(self):
        """Fixture for unit of work mock."""
        yield UnitOfWorkMock()

    @pytest.fixture
    def template_id(self):
        """Fixture for template ID."""
        return uuid4()

    @pytest.fixture
    def section_id(self):
        """Fixture for section ID."""
        return uuid4()

    @pytest.fixture
    def question_id(self):
        """Fixture for question ID."""
        return uuid4()

    @pytest.fixture
    def sample_template(self, template_id):
        """Fixture for a sample template."""
        return TemplateAggregate(
            id=template_id,
            title="Test Template",
            description="A test template",
            status=TemplateStatus.DRAFT,
        )

    @pytest.fixture
    def draft_template(self, template_id, section_id):
        """Fixture for a draft template with a section and question."""
        template = TemplateAggregate(
            id=template_id,
            title="Test Template",
            description="A test template",
            status=TemplateStatus.DRAFT,
        )
        # Add a section with a question to make it publishable
        section = SectionEntity(
            id=section_id,
            title="Test Section",
            description="A test section",
        )
        from app.domain.entities.question import QuestionEntity
        from app.domain.value_objects.question_type import QuestionType

        question = QuestionEntity(
            id=uuid4(),
            text="Test question",
            type=QuestionType.TEXT,
            is_required=True,
        )
        section.questions.append(question)
        template.sections.append(section)
        return template

    @pytest.fixture
    def published_template(self, draft_template):
        """Fixture for a published template."""
        draft_template.publish()
        return draft_template

    @pytest.mark.asyncio
    async def test_create_template_handler_success(self, uow):
        """Test successful template creation."""
        async with uow:
            handler = CreateTemplateHandler(uow)
        command = CreateTemplateCommand(
            title="New Template", description="A new template description"
        )

        template = await handler.handle(command)

        assert template.title == "New Template"
        assert template.description == "A new template description"
        assert template.status == TemplateStatus.DRAFT
        assert template.id is not None
        assert isinstance(template.created_at, datetime)
        assert isinstance(template.updated_at, datetime)
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_create_template_handler_without_description(self, uow):
        """Test template creation without description."""
        async with uow:
            handler = CreateTemplateHandler(uow)
        command = CreateTemplateCommand(title="Template Without Description")

        template = await handler.handle(command)

        assert template.title == "Template Without Description"
        assert template.description is None
        assert template.status == TemplateStatus.DRAFT
        assert template.id is not None
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_publish_template_handler_success(self, uow, draft_template):
        """Test successful template publishing."""
        async with uow:
            handler = PublishTemplateHandler(uow)
        command = PublishTemplateCommand(template_id=draft_template.id)

        # Add template to mock repository
        uow.template.data.append(draft_template)
        original_updated_at = draft_template.updated_at

        template = await handler.handle(command)

        assert template.status == TemplateStatus.PUBLISHED
        assert template.updated_at >= original_updated_at
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_publish_template_handler_not_found(self, uow):
        """Test publishing a non-existent template."""
        async with uow:
            handler = PublishTemplateHandler(uow)
        command = PublishTemplateCommand(template_id=uuid4())

        with pytest.raises(TemplateNotFoundError):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_publish_empty_template_should_fail(self, uow, sample_template):
        """Test publishing an empty template should fail."""
        async with uow:
            handler = PublishTemplateHandler(uow)
        command = PublishTemplateCommand(template_id=sample_template.id)

        # Add template to mock repository
        uow.template.data.append(sample_template)

        # This should raise a ValueError because the template has no questions
        with pytest.raises(ValueError, match="Cannot publish an empty survey template"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_publish_already_published_template_should_fail(
        self, uow, published_template
    ):
        """Test publishing an already published template should fail."""
        async with uow:
            handler = PublishTemplateHandler(uow)
        command = PublishTemplateCommand(template_id=published_template.id)

        # Add template to mock repository
        uow.template.data.append(published_template)

        # This should raise a ValueError because the template is already published
        with pytest.raises(ValueError, match="Template is already published"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_add_section_handler_success(self, uow, sample_template):
        """Test successfully adding a section to a template."""
        async with uow:
            handler = AddSectionHandler(uow)
        command = AddSectionCommand(
            template_id=sample_template.id,
            title="New Section",
            description="A new section description",
        )

        # Add template to mock repository
        uow.template.data.append(sample_template)
        original_section_count = len(sample_template.sections)
        original_updated_at = sample_template.updated_at

        template = await handler.handle(command)

        assert len(template.sections) == original_section_count + 1
        new_section = template.sections[-1]
        assert new_section.title == "New Section"
        assert new_section.description == "A new section description"
        assert template.updated_at > original_updated_at
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_add_section_handler_template_not_found(self, uow):
        """Test adding a section to a non-existent template."""
        async with uow:
            handler = AddSectionHandler(uow)
        command = AddSectionCommand(
            template_id=uuid4(),
            title="New Section",
            description="A new section description",
        )

        with pytest.raises(TemplateNotFoundError):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_add_section_to_published_template_should_fail(
        self, uow, published_template
    ):
        """Test adding a section to a published template should fail."""
        async with uow:
            handler = AddSectionHandler(uow)
        command = AddSectionCommand(
            template_id=published_template.id,
            title="New Section",
            description="A new section description",
        )

        # Add template to mock repository
        uow.template.data.append(published_template)

        # Should raise a ValueError because published templates cannot be edited
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_add_question_handler_success(self, uow, sample_template, section_id):
        """Test successfully adding a question to a section."""
        async with uow:
            handler = AddQuestionHandler(uow)
        command = AddQuestionCommand(
            template_id=sample_template.id,
            section_id=section_id,
            question_text="How would you rate our service?",
            question_type="single_choice",
            options=["Excellent", "Good", "Average", "Poor"],
            required=True,
        )

        # Add a section to the template
        section = SectionEntity(id=section_id, title="Test Section")
        sample_template.sections.append(section)
        uow.template.data.append(sample_template)

        template = await handler.handle(command)

        # Verify the question was added
        section = template.sections[0]
        assert len(section.questions) == 1
        question = section.questions[0]
        assert question.text == "How would you rate our service?"
        assert question.type.value == "single_choice"
        assert len(question.options) == 4
        assert question.is_required is True
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_add_question_handler_template_not_found(self, uow, section_id):
        """Test adding a question to a non-existent template."""
        async with uow:
            handler = AddQuestionHandler(uow)
        command = AddQuestionCommand(
            template_id=uuid4(),
            section_id=section_id,
            question_text="Test question",
            question_type="text",
            required=True,
        )

        with pytest.raises(TemplateNotFoundError):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_add_question_handler_without_options(
        self, uow, sample_template, section_id
    ):
        """Test adding a question without options."""
        async with uow:
            handler = AddQuestionHandler(uow)
        command = AddQuestionCommand(
            template_id=sample_template.id,
            section_id=section_id,
            question_text="What is your name?",
            question_type="text",
            required=False,
        )

        # Add a section to the template
        section = SectionEntity(id=section_id, title="Test Section")
        sample_template.sections.append(section)
        uow.template.data.append(sample_template)

        template = await handler.handle(command)

        # Verify the question was added
        section = template.sections[0]
        assert len(section.questions) == 1
        question = section.questions[0]
        assert question.text == "What is your name?"
        assert question.type.value == "text"
        assert question.options is None
        assert question.is_required is False
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_edit_question_handler_success(
        self, uow, sample_template, section_id, question_id
    ):
        """Test successfully editing a question."""
        async with uow:
            handler = EditQuestionHandler(uow)
        command = EditQuestionCommand(
            template_id=sample_template.id,
            section_id=section_id,
            question_id=question_id,
            question_text="Updated question text",
            question_type="multiple_choice",
            options=["Option A", "Option B", "Option C"],
            required=False,
        )

        # Add a section with a question to the template
        section = SectionEntity(id=section_id, title="Test Section")
        from app.domain.entities.question import QuestionEntity
        from app.domain.value_objects.question_type import QuestionType

        question = QuestionEntity(
            id=question_id,
            text="Original question text",
            type=QuestionType.TEXT,
            is_required=True,
        )
        section.questions.append(question)
        sample_template.sections.append(section)
        uow.template.data.append(sample_template)

        template = await handler.handle(command)

        # Verify the question was updated
        section = template.sections[0]
        assert len(section.questions) == 1
        question = section.questions[0]
        assert question.text == "Updated question text"
        assert question.type.value == "multiple_choice"
        assert len(question.options) == 3
        assert question.is_required is False
        assert uow._committed is True

    @pytest.mark.asyncio
    async def test_edit_question_handler_template_not_found(
        self, uow, section_id, question_id
    ):
        """Test editing a question in a non-existent template."""
        async with uow:
            handler = EditQuestionHandler(uow)
        command = EditQuestionCommand(
            template_id=uuid4(),
            section_id=section_id,
            question_id=question_id,
            question_text="Updated question",
            question_type="text",
            required=True,
        )

        with pytest.raises(TemplateNotFoundError):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_handler_integration_workflow(self, uow):
        """Test complete wf: create template, add section, add question, publish."""
        async with uow:
            # Step 1: Create template
            create_handler = CreateTemplateHandler(uow)
            create_command = CreateTemplateCommand(
                title="Workflow Template", description="Test workflow"
            )
            template = await create_handler.handle(create_command)
            assert template.status == TemplateStatus.DRAFT
            assert len(template.sections) == 0

            # Step 2: Add section
            add_section_handler = AddSectionHandler(uow)
            add_section_command = AddSectionCommand(
                template_id=template.id,
                title="Workflow Section",
                description="Test section",
            )
            template = await add_section_handler.handle(add_section_command)
            assert len(template.sections) == 1

            # Step 3: Add question
            add_question_handler = AddQuestionHandler(uow)
            add_question_command = AddQuestionCommand(
                template_id=template.id,
                section_id=template.sections[0].id,
                question_text="Workflow question",
                question_type="text",
                required=True,
            )
            template = await add_question_handler.handle(add_question_command)
            assert len(template.sections[0].questions) == 1

            # Step 4: Publish template
            publish_handler = PublishTemplateHandler(uow)
            publish_command = PublishTemplateCommand(template_id=template.id)
            template = await publish_handler.handle(publish_command)
            assert template.status == TemplateStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_handler_error_handling(self, uow):
        """Test proper error handling in handlers."""
        # Test with non-existent template IDs
        non_existent_id = uuid4()

        async with uow:
            # Test publish handler
            publish_handler = PublishTemplateHandler(uow)
            publish_command = PublishTemplateCommand(template_id=non_existent_id)
            with pytest.raises(TemplateNotFoundError):
                await publish_handler.handle(publish_command)

            # Test add section handler
            add_section_handler = AddSectionHandler(uow)
            add_section_command = AddSectionCommand(
                template_id=non_existent_id, title="Test", description="Test"
            )
            with pytest.raises(TemplateNotFoundError):
                await add_section_handler.handle(add_section_command)

            # Test add question handler
            add_question_handler = AddQuestionHandler(uow)
            add_question_command = AddQuestionCommand(
                template_id=non_existent_id,
                section_id=uuid4(),
                question_text="Test",
                question_type="text",
                required=True,
            )
            with pytest.raises(TemplateNotFoundError):
                await add_question_handler.handle(add_question_command)

    @pytest.mark.asyncio
    async def test_handler_data_consistency(self, uow, sample_template):
        """Test that handlers maintain data consistency."""
        # Add template to mock repository
        async with uow:
            uow.template.data.append(sample_template)

            # Verify template exists
            retrieved_template = await uow.template.get_by_id(sample_template.id)
            assert retrieved_template.id == sample_template.id
            assert retrieved_template.title == sample_template.title

            # Add section using handler
            add_section_handler = AddSectionHandler(uow)
            add_section_command = AddSectionCommand(
                template_id=sample_template.id,
                title="Consistency Test",
                description="Test",
            )
            updated_template = await add_section_handler.handle(add_section_command)

            # Verify the template was updated correctly
            assert len(updated_template.sections) == 1
            assert updated_template.sections[0].title == "Consistency Test"
