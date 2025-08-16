from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.aggregates.template import TemplateAggregate
from app.domain.entities.question import QuestionEntity
from app.domain.entities.section import SectionEntity
from app.domain.value_objects.question_options import QuestionOption
from app.domain.value_objects.question_type import QuestionType
from app.domain.value_objects.template_status import TemplateStatus


class TestTemplateAggregate:
    """Test cases for TemplateAggregate domain aggregate."""

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
        """Fixture for a basic template in DRAFT status."""
        return TemplateAggregate(
            id=template_id,
            title="Test Template",
            description="A test template",
            status=TemplateStatus.DRAFT,
        )

    @pytest.fixture
    def sample_section(self, section_id):
        """Fixture for a sample section."""
        return SectionEntity(
            id=section_id, title="Test Section", description="A test section"
        )

    @pytest.fixture
    def sample_question(self, question_id):
        """Fixture for a sample question."""
        return QuestionEntity(
            id=question_id,
            text="What is your favorite color?",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption(label="Red", value="red", order=1),
                QuestionOption(label="Blue", value="blue", order=2),
                QuestionOption(label="Green", value="green", order=3),
            ],
            is_required=True,
        )

    @pytest.fixture
    def published_template(self, template_id, section_id, question_id):
        """Fixture for a published template with questions."""
        section = SectionEntity(
            id=section_id, title="Test Section", description="A test section"
        )
        question = QuestionEntity(
            id=question_id,
            text="What is your favorite color?",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption(label="Red", value="red", order=1),
                QuestionOption(label="Blue", value="blue", order=2),
            ],
            is_required=True,
        )
        section.questions.append(question)

        template = TemplateAggregate(
            id=template_id,
            title="Test Template",
            description="A test template",
            status=TemplateStatus.DRAFT,
        )
        template.sections.append(section)
        template.publish()
        return template

    @pytest.fixture
    def archived_template(self, template_id):
        """Fixture for an archived template."""
        return TemplateAggregate(
            id=template_id,
            title="Test Template",
            description="A test template",
            status=TemplateStatus.ARCHIVED,
        )

    def test_template_creation(self, template_id):
        """Test template creation with default values."""
        template = TemplateAggregate(
            id=template_id, title="Test Template", description="A test template"
        )

        assert template.id == template_id
        assert template.title == "Test Template"
        assert template.description == "A test template"
        assert template.status == TemplateStatus.DRAFT
        assert template.sections == []
        assert isinstance(template.created_at, datetime)
        assert isinstance(template.updated_at, datetime)

    def test_template_creation_without_id(self):
        """Test template creation without providing an ID."""
        template = TemplateAggregate(
            title="Test Template", description="A test template"
        )

        assert template.id is None
        assert template.title == "Test Template"
        assert template.status == TemplateStatus.DRAFT

    def test_publish_success(self, sample_template, sample_section, sample_question):
        """Test successful template publishing."""
        # Add section and question
        sample_section.questions.append(sample_question)
        sample_template.sections.append(sample_section)

        # Store original updated_at
        original_updated_at = sample_template.updated_at

        # Publish template
        sample_template.publish()

        assert sample_template.status == TemplateStatus.PUBLISHED
        assert sample_template.updated_at > original_updated_at

    def test_publish_already_published(self, published_template):
        """Test publishing an already published template."""
        with pytest.raises(ValueError, match="Template is already published"):
            published_template.publish()

    def test_publish_archived_template(self, archived_template):
        """Test publishing an archived template."""
        with pytest.raises(ValueError, match="Cannot publish an archived template"):
            archived_template.publish()

    def test_publish_empty_template(self, sample_template):
        """Test publishing a template without questions."""
        with pytest.raises(ValueError, match="Cannot publish an empty survey template"):
            sample_template.publish()

    def test_publish_template_with_empty_sections(
        self, sample_template, sample_section
    ):
        """Test publishing a template with sections but no questions."""
        sample_template.sections.append(sample_section)

        with pytest.raises(ValueError, match="Cannot publish an empty survey template"):
            sample_template.publish()

    def test_add_section_success(self, sample_template, sample_section):
        """Test successfully adding a section to a draft template."""
        original_updated_at = sample_template.updated_at
        original_section_count = len(sample_template.sections)

        sample_template.add_section(sample_section)

        assert len(sample_template.sections) == original_section_count + 1
        assert sample_template.sections[-1] == sample_section
        assert sample_template.updated_at > original_updated_at

    def test_add_section_to_published_template(
        self, published_template, sample_section
    ):
        """Test adding a section to a published template."""
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.add_section(sample_section)

    def test_add_section_to_archived_template(self, archived_template, sample_section):
        """Test adding a section to an archived template."""
        with pytest.raises(ValueError, match="Cannot edit an archived template"):
            archived_template.add_section(sample_section)

    def test_add_question_success(
        self, sample_template, sample_section, sample_question
    ):
        """Test successfully adding a question to a section."""
        sample_template.sections.append(sample_section)
        original_updated_at = sample_template.updated_at
        original_question_count = len(sample_section.questions)

        sample_template.add_question(sample_section.id, sample_question)

        assert len(sample_section.questions) == original_question_count + 1
        assert sample_section.questions[-1] == sample_question
        assert sample_template.updated_at > original_updated_at

    def test_add_question_section_not_found(self, sample_template, sample_question):
        """Test adding a question to a non-existent section."""
        non_existent_section_id = uuid4()

        with pytest.raises(
            ValueError, match=f"Section {non_existent_section_id} not found"
        ):
            sample_template.add_question(non_existent_section_id, sample_question)

    def test_add_question_to_published_template(
        self, published_template, sample_question
    ):
        """Test adding a question to a published template."""
        section_id = published_template.sections[0].id

        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.add_question(section_id, sample_question)

    def test_add_question_to_archived_template(
        self, archived_template, sample_section, sample_question
    ):
        """Test adding a question to an archived template."""
        archived_template.sections.append(sample_section)

        with pytest.raises(ValueError, match="Cannot edit an archived template"):
            archived_template.add_question(sample_section.id, sample_question)

    def test_edit_question_success(
        self, sample_template, sample_section, sample_question
    ):
        """Test successfully editing a question."""
        sample_template.sections.append(sample_section)
        sample_section.questions.append(sample_question)

        original_updated_at = sample_template.updated_at

        # Create updated question
        updated_question = QuestionEntity(
            id=sample_question.id,
            text="Updated question text",
            type=QuestionType.TEXT,
            is_required=False,
        )

        sample_template.edit_question(
            sample_section.id, sample_question.id, updated_question
        )

        # Verify the question was updated
        edited_question = sample_section.questions[0]
        assert edited_question.text == "Updated question text"
        assert edited_question.type == QuestionType.TEXT
        assert edited_question.is_required is False
        assert sample_template.updated_at > original_updated_at

    def test_edit_question_section_not_found(self, sample_template, sample_question):
        """Test editing a question in a non-existent section."""
        non_existent_section_id = uuid4()
        question_id = uuid4()

        with pytest.raises(
            ValueError, match=f"Section {non_existent_section_id} not found"
        ):
            sample_template.edit_question(
                non_existent_section_id, question_id, sample_question
            )

    def test_edit_question_not_found(
        self, sample_template, sample_section, sample_question
    ):
        """Test editing a non-existent question."""
        sample_template.sections.append(sample_section)
        non_existent_question_id = uuid4()

        with pytest.raises(
            ValueError, match=f"Question {non_existent_question_id} not found"
        ):
            sample_template.edit_question(
                sample_section.id, non_existent_question_id, sample_question
            )

    def test_edit_question_in_published_template(
        self, published_template, sample_question
    ):
        """Test editing a question in a published template."""
        section_id = published_template.sections[0].id
        question_id = published_template.sections[0].questions[0].id

        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.edit_question(section_id, question_id, sample_question)

    def test_edit_question_in_archived_template(
        self, archived_template, sample_section, sample_question
    ):
        """Test editing a question in an archived template."""
        archived_template.sections.append(sample_section)
        sample_section.questions.append(sample_question)

        with pytest.raises(ValueError, match="Cannot edit an archived template"):
            archived_template.edit_question(
                sample_section.id, sample_question.id, sample_question
            )

    def test_can_edit_draft_template(self, sample_template):
        """Test that draft templates can be edited."""
        # This should not raise any exception
        sample_template._can_edit()

    def test_cannot_edit_published_template(self, published_template):
        """Test that published templates cannot be edited."""
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template._can_edit()

    def test_cannot_edit_archived_template(self, archived_template):
        """Test that archived templates cannot be edited."""
        with pytest.raises(ValueError, match="Cannot edit an archived template"):
            archived_template._can_edit()

    def test_template_with_multiple_sections_and_questions(self, template_id):
        """Test template with multiple sections and questions."""
        template = TemplateAggregate(
            id=template_id,
            title="Complex Template",
            description="A template with multiple sections",
        )

        # Add first section
        section1 = SectionEntity(
            id=uuid4(), title="Section 1", description="First section"
        )
        question1 = QuestionEntity(
            id=uuid4(), text="Question 1", type=QuestionType.TEXT, is_required=True
        )
        section1.questions.append(question1)
        template.add_section(section1)

        # Add second section
        section2 = SectionEntity(
            id=uuid4(), title="Section 2", description="Second section"
        )
        question2 = QuestionEntity(
            id=uuid4(),
            text="Question 2",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption(label="Option 1", value="opt1", order=1),
                QuestionOption(label="Option 2", value="opt2", order=2),
            ],
            is_required=False,
        )
        section2.questions.append(question2)
        template.add_section(section2)

        # Add another question to first section
        question3 = QuestionEntity(
            id=uuid4(), text="Question 3", type=QuestionType.NUMBER, is_required=True
        )
        template.add_question(section1.id, question3)

        # Verify structure
        assert len(template.sections) == 2
        assert len(template.sections[0].questions) == 2
        assert len(template.sections[1].questions) == 1

        # Publish template
        template.publish()
        assert template.status == TemplateStatus.PUBLISHED

    def test_template_immutability_after_publishing(self, published_template):
        """Test that published templates cannot be modified."""
        # Try to add a section
        new_section = SectionEntity(
            id=uuid4(), title="New Section", description="A new section"
        )
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.add_section(new_section)

        # Try to add a question
        new_question = QuestionEntity(
            id=uuid4(), text="New Question", type=QuestionType.TEXT, is_required=True
        )
        section_id = published_template.sections[0].id
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.add_question(section_id, new_question)

        # Try to edit a question
        question_id = published_template.sections[0].questions[0].id
        with pytest.raises(ValueError, match="Cannot edit a published template"):
            published_template.edit_question(section_id, question_id, new_question)

    def test_template_status_transitions(
        self, sample_template, sample_section, sample_question
    ):
        """Test template status transitions."""
        # Start with DRAFT
        assert sample_template.status == TemplateStatus.DRAFT

        # Add content and publish
        sample_section.questions.append(sample_question)
        sample_template.sections.append(sample_section)
        sample_template.publish()
        assert sample_template.status == TemplateStatus.PUBLISHED

        # Cannot go back to DRAFT
        # (no method for this, but status is immutable after publishing)
        # Cannot publish again
        with pytest.raises(ValueError, match="Template is already published"):
            sample_template.publish()

    def test_template_with_different_question_types(self, template_id):
        """Test template with various question types."""
        template = TemplateAggregate(
            id=template_id,
            title="Multi-Type Template",
            description="Template with different question types",
        )

        section = SectionEntity(
            id=uuid4(),
            title="Mixed Questions",
            description="Section with various question types",
        )

        # Add different question types
        questions = [
            QuestionEntity(
                id=uuid4(),
                text="Text question",
                type=QuestionType.TEXT,
                is_required=True,
            ),
            QuestionEntity(
                id=uuid4(),
                text="Number question",
                type=QuestionType.NUMBER,
                is_required=False,
            ),
            QuestionEntity(
                id=uuid4(),
                text="Single choice question",
                type=QuestionType.SINGLE_CHOICE,
                options=[
                    QuestionOption(label="Yes", value="yes", order=1),
                    QuestionOption(label="No", value="no", order=2),
                ],
                is_required=True,
            ),
            QuestionEntity(
                id=uuid4(),
                text="Multiple choice question",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    QuestionOption(label="Option A", value="a", order=1),
                    QuestionOption(label="Option B", value="b", order=2),
                    QuestionOption(label="Option C", value="c", order=3),
                ],
                is_required=False,
            ),
        ]

        for question in questions:
            section.questions.append(question)

        template.sections.append(section)

        # Verify all questions were added
        assert len(template.sections[0].questions) == 4

        # Publish template
        template.publish()
        assert template.status == TemplateStatus.PUBLISHED
