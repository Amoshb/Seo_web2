import unittest
from flask import Flask
from flask_testing import TestCase
from websites import app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_route(self):
        # Send GET request to home route
        response = self.client.get('/home')
        self.assert_template_used('home.html')
        self.assertEqual(response.status_code, 200)

    def test_table_page(self):
        response = self.client.get('/tables')
        self.assert_template_used('tables.html')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
