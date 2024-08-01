from app import app, db
import unittest
import json

class BookTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_create_book(self):
        response = self.app.post('/api/books', json={
            "title": "Test Book",
            "author": "Test Author",
            "year": 2020
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(response.json['title'], 'Test Book')
        self.assertEqual(response.json['author'], 'Test Author')
        self.assertEqual(response.json['year'], 2020)
        