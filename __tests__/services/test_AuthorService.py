from unittest import TestCase
from unittest.mock import create_autospec, patch

from repositories.MealRepository import MealRepository
from repositories.BookRepository import BookRepository
from services.MealService import MealService


class TestAuthorService(TestCase):
    authorRepository: MealRepository
    authorService: MealService

    def setUp(self):
        super().setUp()
        self.authorRepository = create_autospec(
            MealRepository
        )
        self.authorRepository = create_autospec(
            BookRepository
        )
        self.authorService = MealService(
            self.authorRepository
        )

    @patch(
        "schemas.pydantic.AuthorSchema.AuthorSchema",
        autospec=True,
    )
    def test_create(self, AuthorSchema):
        author = AuthorSchema()
        author.name = "JK Rowling"

        self.authorService.create(author)

        # Should call create method on Author Repository
        self.authorRepository.create.assert_called_once()

    def test_delete(self):
        self.authorService.delete(meal_id=1)

        # Should call delete method on Author Repository
        self.authorRepository.delete.assert_called_once()

    def test_get(self):
        self.authorService.get(author_id=1)

        # Should call get method on Author Repository
        self.authorRepository.get.assert_called_once()

    def test_list(self):
        name = "Rowling"
        pageSize = 10
        startIndex = 2

        self.authorService.list_by_user_id(name, pageSize, startIndex)

        # Should call list method on Author Repository
        self.authorRepository.list_by_user_id.assert_called_once_with(
            name, pageSize, startIndex
        )

    @patch(
        "schemas.pydantic.AuthorSchema.AuthorSchema",
        autospec=True,
    )
    def test_update(self, AuthorSchema):
        author = AuthorSchema()
        author.name = "JRR Tokein"

        self.authorService.update(
            author_id=1, author_body=author
        )

        # Should call update method on Book Repository
        self.authorRepository.update.assert_called_once()
