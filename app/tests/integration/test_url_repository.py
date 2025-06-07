from unittest import TestCase
from uuid import uuid4
from datetime import datetime
from app.domain.services.database_service import DatabaseService
from app.adapters.output.repositories.url_repository_adapter import URLRepositoryAdapter
from app.adapters.output.repositories.user_repository_adapter import UserRepositoryAdapter
from app.domain.entities.url import URLCreateDTO
from app.domain.entities.user import UserAuthenticateDTO

class TestURLRepository(TestCase):

    def setUp(self):
        self.db_service = DatabaseService()
        self.user_repository = UserRepositoryAdapter(db_service=self.db_service)
        self.repository = URLRepositoryAdapter(db_service=self.db_service)

        self.user_payload = UserAuthenticateDTO(
            email=f'{uuid4()}@test.com',
            password='testpassword'
        )
        self.user = self.user_repository.create(self.user_payload)
        self.current_user_id = self.user.id

        self.payload = URLCreateDTO(raw_url="https://example.com")
        self.shortened_url = f"ex{uuid4().hex[:6]}"

    def test_create_url(self):
        created_url = self.repository.create(
            payload=self.payload,
            current_user_id=self.current_user_id,
            shortened_url=self.shortened_url
        )

        self.assertIsNotNone(created_url)
        self.assertEqual(created_url.shortened_url, self.shortened_url)

        self.repository.delete_by_shortened_url(self.shortened_url)

    def test_get_one_url(self):
        created_url = self.repository.create(
            payload=self.payload,
            current_user_id=self.current_user_id,
            shortened_url=self.shortened_url
        )

        retrieved_url = self.repository.get_one(shortened_url=self.shortened_url)

        self.assertIsNotNone(retrieved_url)
        self.assertEqual(retrieved_url.shortened_url, self.shortened_url)
        self.assertEqual(retrieved_url.raw_url, self.payload.raw_url)
        self.assertEqual(retrieved_url.created_by, self.current_user_id)
        self.assertIsInstance(retrieved_url.created_at, datetime)
        self.assertFalse(retrieved_url.deleted)

        self.repository.delete_by_shortened_url(self.shortened_url)

    def test_get_all_urls(self):
        url1 = self.repository.create(
            payload=self.payload,
            current_user_id=self.current_user_id,
            shortened_url=self.shortened_url
        )

        urls = self.repository.get_all()
        self.assertIsInstance(urls, list)
        self.assertTrue(any(u.shortened_url == self.shortened_url for u in urls))

        self.repository.delete_by_shortened_url(self.shortened_url)

    def test_delete_by_shortened_url(self):
        created_url = self.repository.create(
            payload=self.payload,
            current_user_id=self.current_user_id,
            shortened_url=self.shortened_url
        )

        deleted_url = self.repository.delete_by_shortened_url(self.shortened_url)

        self.assertIsNotNone(deleted_url)
        self.assertEqual(deleted_url.shortened_url, self.shortened_url)

        result = self.repository.get_one(self.shortened_url)
        self.assertIsNone(result)
