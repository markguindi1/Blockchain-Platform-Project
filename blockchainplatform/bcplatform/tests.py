from django.test import TestCase, Client
import unittest
from .views import *
from .models import *
# Create your tests here.

class Basetest(unittest.TestCase):
    """ Base test case. Each test case class below should inherit from this class, as this class takes care of certain
    common steps in the setUp method, such as setting up the test Client. The steps of each test should be handled in
    the test_details() method.
    """

    def setUp(self):
        self.client = Client()

        username = "testuser"
        email = "mag868@nyu.edu"
        password = "12345"

        # To do: Change the below code to work for our app
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
        self.user = User.objects.get(username=username)
        is_logged_in = self.client.login(username=username, password=password)
        # print("Logged in status:", is_logged_in)

    def test_details(self):
        pass
