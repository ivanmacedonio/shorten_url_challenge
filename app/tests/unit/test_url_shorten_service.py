import unittest
import uuid
import json
from unittest.mock import MagicMock
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.domain.services.url_shorten_service import URLShortenService
from app.domain.ports.input.url_service_port import URLServicePort
from app.domain.entities.url import URLCreateDTO, URLPartialRetrieveDTO
from app.domain.utils.base62_encoder import generate_random_short_id, parse_number_to_base62

class TestURLShortenService(unittest.TestCase):
    
    def setUp(self):
        self.mocked_repository = MagicMock()
        self.mocked_service: URLServicePort = URLShortenService(repository=self.mocked_repository)
    
    def test_get_url_redirects_successfully(self):
        mock_url = MagicMock()
        mock_url.raw_url = "https://www.twitch.tv/"
        self.mocked_repository.get_one.return_value = mock_url
        response = self.mocked_service.get_url_and_redirect(
            shortened_url="testshortid"
        )
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "https://www.twitch.tv/")
    
    def test_get_all_urls(self):
        url_1 = MagicMock()
        url_2 = MagicMock()
        url_3 = MagicMock()
        
        url_1.to_dict.return_value = {"shortened_url": "abc", "raw_url": "https://1.com"}
        url_2.to_dict.return_value = {"shortened_url": "abc", "raw_url": "https://2.com"}
        url_3.to_dict.return_value = {"shortened_url": "abc", "raw_url": "https://3.com"}
        
        self.mocked_repository.get_all.return_value = [url_1, url_2, url_3]
        response = self.mocked_service.get_all()
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_save_url(self):
        mocked_user_id = uuid.uuid4()
        mocked_url = "https://google.com"
        self.mocked_repository.get_one.return_value = None
        self.mocked_repository.create.return_value = URLPartialRetrieveDTO(
            id=uuid.uuid4(),
            shortened_url="abc123"
        )
        
        response = self.mocked_service.save_url(current_user_id=mocked_user_id, payload=URLCreateDTO(raw_url=mocked_url))
        parsed_body = json.loads(response.body.decode())
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(parsed_body['shortened_url'], "abc123")
    
    def test_save_url_raises_if_shortened_url_is_taken(self):
        mocked_user_id = uuid.uuid4()
        mocked_url = "https://google.com"
        self.mocked_repository.get_one.return_value = MagicMock()
        self.mocked_repository.create.return_value = URLPartialRetrieveDTO(
            id=uuid.uuid4(),
            shortened_url="abc123"
        )
        
        with self.assertRaises(HTTPException) as e:
            response = self.mocked_service.save_url(current_user_id=mocked_user_id, payload=URLCreateDTO(raw_url=mocked_url))
            parsed_body = json.loads(response.body.decode())
            
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 404)
            
    def test_delete_url(self):
        mocked_url = MagicMock()
        mocked_shortened_id = "abc123"
        self.mocked_repository.delete_by_shortened_url.return_value = mocked_url
        response = self.mocked_service.delete(mocked_shortened_id)
        
        parsed_body = json.loads(response.body.decode())
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_body['message'], "URL with shortenedID abc123 deleted successfully")
    
    def test_delete_url_raises_if_url_doesnt_exists(self):
        mocked_shortened_id = "abc123"
        self.mocked_repository.delete_by_shortened_url.return_value = None
        with self.assertRaises(HTTPException) as e:
            response = self.mocked_service.delete(mocked_shortened_id)
            parsed_body = json.loads(response.body.decode())
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(parsed_body['message'], "URL with shortened ID abc123 not found or was already deleted")
        
    def test_generate_random_short_id_length(self):
        short_id = generate_random_short_id()
        self.assertIsInstance(short_id, str)
        self.assertEqual(len(short_id), 12)

    def test_generate_random_short_id_uniqueness(self):
        ids = {generate_random_short_id() for _ in range(1000)}
        self.assertEqual(len(ids), 1000)

    def test_parse_uuid4_as_int(self):
        u = uuid.uuid4()
        n = u.int
        base62 = parse_number_to_base62(n)
        self.assertIsInstance(base62, str)
        self.assertGreater(len(base62), 0)
    
    def test_parse_invalid_type(self):
        with self.assertRaises(TypeError):
            parse_number_to_base62("not an integer typpe")
        


        