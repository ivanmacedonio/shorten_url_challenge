import unittest
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from jose import jwt
from uuid import uuid4
from app.domain.services.jwt_service import JWTService
from app.domain.configs.dependencies import JWT_SECRET_KEY, JWT_EXPIRATION_TIME


class TestJWTService(unittest.TestCase):

    def setUp(self):
        self.jwt_service = JWTService()
        self.subject = uuid4()

    def test_create_access_token(self):
        token = self.jwt_service.create_access_token(self.subject)
        self.assertIsInstance(token, str)

        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], str(self.subject))
        self.assertIn("exp", decoded)

    def test_verify_access_token_success(self):
        token = self.jwt_service.create_access_token(self.subject)
        subject = self.jwt_service.verify_access_token(token)
        self.assertEqual(subject, str(self.subject))

    def test_verify_access_token_invalid_token(self):
        invalid_token = "invalid.token.string"
        with self.assertRaises(HTTPException) as context:
            self.jwt_service.verify_access_token(invalid_token)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("invalid access token", context.exception.detail["message"])

    def test_verify_access_token_missing_subject(self):
        exp = datetime.now(timezone.utc) + timedelta(minutes=5)
        token_without_sub = jwt.encode({"exp": exp}, JWT_SECRET_KEY, algorithm="HS256")
        
        with self.assertRaises(HTTPException) as context:
            self.jwt_service.verify_access_token(token_without_sub)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("subject is missing", context.exception.detail["detail"])

    def test_verify_access_token_expired(self):
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
        expired_token = jwt.encode({"sub": str(self.subject), "exp": expired_time}, JWT_SECRET_KEY, algorithm="HS256")
        
        with self.assertRaises(HTTPException) as context:
            self.jwt_service.verify_access_token(expired_token)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("invalid access token, please login again",
                      context.exception.detail["message"])