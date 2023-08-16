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

    def test_currency_page(self):
        response = self.client.get('/currency')
        self.assert_template_used('currency.html')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assert_template_used('register.html')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assert_template_used('login.html')
        self.assertEqual(response.status_code, 200)

    def test_userhome_page(self):
        response = self.client.get('/userhome')
        self.assert_template_used('Userlayout.html')
        self.assertEqual(response.status_code, 200)

    def test_userchat_page(self):
        response = self.client.get('/userchart')
        self.assert_template_used('userchart.html')
        self.assertEqual(response.status_code, 200)

    def test_usercurrency_page(self):
        response = self.client.get('/usercurrency')
        self.assert_template_used('usercurrency.html')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
