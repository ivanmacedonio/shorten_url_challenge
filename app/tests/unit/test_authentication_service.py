import unittest
import json
import uuid
from passlib.hash import bcrypt
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.domain.services.authentication_service import AuthenticationService
from app.domain.entities.user import UserAuthenticateDTO, PartialUserRetrieveDTO

class TestAuhenticationService(unittest.TestCase):

    def setUp(self):
        self.mocked_repository = MagicMock()
        self.mocked_token_service = MagicMock()
        self.mocked_authentication_service = AuthenticationService(
            jwt_service=self.mocked_token_service,
            user_repository=self.mocked_repository
        )
        
        self.mocked_db_user = PartialUserRetrieveDTO(
            id=uuid.uuid4(),
            email="test@test.com",
            password=bcrypt.hash("testpassword")
        )
        
        self.mocked_auth_payload = UserAuthenticateDTO(
            email="test@test.com",
            password="testpassword"
        )
        
    def test_login_works_successfully(self):
        self.mocked_repository.get_by_email.return_value = self.mocked_db_user
        self.mocked_token_service.create_access_token.return_value = "test_token"
        response = self.mocked_authentication_service.login(self.mocked_auth_payload)
        parsed_body = json.loads(response.body.decode())
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_body['token_type'], 'Bearer')
        self.assertEqual(parsed_body['access_token'], 'test_token')
        self.assertEqual(parsed_body['message'], 'user authenticated successfully')
        