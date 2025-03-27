from django.test import TestCase
from django.test.client import Client
from scrapchef.models import User


# Create your tests here.
class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="testuser", password="testuser")

    def test_login_get(self):
        response = self.client.get("/login/")
        self.assertTrue(b"Sign In" in response.content)
        self.assertEqual(response.status_code, 200)

    def test_login_post_failed(self):
        response = self.client.post("/login/", data={"username": "invalid", "password": "invalid"})
        self.assertEqual(b"Invalid username or password.", response.content)
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post("/login/", data={"username": "testuser", "password": "testuser"})
        self.assertEqual(response.status_code, 302)


class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="testuser", password="testuser")

    def test_signup_failed_1(self):
        response = self.client.post("/signup/", data={"username": "test"})
        self.assertEqual(response.status_code, 302)

    def test_signup_failed_2(self):
        response = self.client.post("/signup/", data={"username": "testuser", "password": "test"})
        self.assertEqual(response.status_code, 302)


class TestIfNotLogin(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="testuser", password="testuser")

    def test_dashboard(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_upload_post(self):
        response = self.client.post("/upload/")
        self.assertEqual(response.status_code, 302)


class TestIfLogin(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="testuser", password="testuser")
        self.client.post("/login/", data={"username": "testuser", "password": "testuser"})

    def test_dashboard(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        response = self.client.post("/upload/")
        self.assertEqual(response.status_code, 302)
        response = self.client.post("/upload/", data={"url": "testurl"})
        self.assertEqual(response.status_code, 302)
