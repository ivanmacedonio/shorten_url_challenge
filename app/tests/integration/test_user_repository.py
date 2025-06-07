from unittest import TestCase
import json
from uuid import uuid4
from app.domain.services.database_service import DatabaseService
from app.adapters.output.repositories.user_repository_adapter import UserRepositoryAdapter
from app.domain.services.user_service import UserService
from app.domain.entities.user import UserAuthenticateDTO, PartialUserRetrieveDTO, UserRetrieveDTO

class TestUserRepository(TestCase):
    
    def setUp(self):
        self.repository = UserRepositoryAdapter(db_service=DatabaseService())
        self.users_service = UserService(repository=self.repository) 
        self.user_payload = UserAuthenticateDTO(
            email=f'{uuid4()}@test.com',
            password="testpassword"
        )

    def test_get_all(self):
        response = self.users_service.get_all()
        parsed_body = json.loads(response.body.decode())
        
        self.assertIsNotNone(parsed_body)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(parsed_body["results"], list))
        
    def test_register_user(self):
        created_user: PartialUserRetrieveDTO = self.repository.create(self.user_payload)
        
        self.assertIsNotNone(created_user)
        self.assertIsNotNone(created_user.id)
        self.assertIsNotNone(created_user.email)
        self.assertIsNotNone(created_user.password)

        self.repository.delete(user_id=created_user.id)
    
    def test_get_user_by_id(self):
        created_user = self.repository.create(self.user_payload)
        
        user: UserRetrieveDTO = self.repository.get_by_id(user_id=created_user.id)
        
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.deleted)

        self.repository.delete(user_id=created_user.id)
        
    def test_delete_user_soft(self):
        created_user = self.repository.create(self.user_payload)

        deleted_user = self.repository.delete(created_user.id)

        self.assertIsNotNone(deleted_user)
        self.assertEqual(deleted_user.id, created_user.id)
        self.assertEqual(deleted_user.email, created_user.email)

        should_be_none = self.repository.get_by_id(created_user.id)
        self.assertIsNone(should_be_none)

    def test_get_user_already_exists_by_email(self):
        self.assertFalse(
            self.repository.get_user_already_exists_by_email(self.user_payload.email)
        )

        created_user = self.repository.create(self.user_payload)

        self.assertTrue(
            self.repository.get_user_already_exists_by_email(created_user.email)
        )

        self.repository.delete(created_user.id)

    def test_get_by_email(self):
        created_user = self.repository.create(self.user_payload)

        user = self.repository.get_by_email(created_user.email)

        self.assertIsNotNone(user)
        self.assertEqual(user.email, created_user.email)
        self.assertEqual(user.id, created_user.id)

        self.repository.delete(created_user.id)
        user_after_delete = self.repository.get_by_email(created_user.email)
        self.assertIsNone(user_after_delete)
