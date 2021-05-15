import pytest
import unittest
from app.models import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash)
