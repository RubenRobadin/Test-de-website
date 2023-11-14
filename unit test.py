from website import app
from website.customers.routes import customerLogin
import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application context before each test method is run
        self.app = app.test_client()  # Create a test client for making requests
        self.context = app.app_context()
        self.context.push()
        app.config['TESTING'] = True  # Set testing mode to True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing

    def tearDown(self):
        # Pop the Flask application context after each test method is run
        self.context.pop()

    def test_valid_login(self):
        response = self.app.post('/login', data=dict(
            email='rubenrobadin@hotmail.com',
            password='12345678'
        ), follow_redirects=True)

        self.assertIn(b'Add to Cart', response.data, "Valid login should redirect to the home page")

    def test_invalid_username(self):
        response = self.app.post('/login', data=dict(
            email='invalid_username@example.com',
            password='pepe5'
        ), follow_redirects=True)
        self.assertIn(b'Incorrect email or password', response.data, "Invalid username should show error message")

    def test_invalid_password(self):
        response = self.app.post('/login', data=dict(
            email='pepe5@email.com',
            password='invalid_password'
        ), follow_redirects=True)
        self.assertIn(b'Incorrect email or password', response.data, "Invalid password should show error message")

    def test_empty_fields(self):
        response = self.app.post('/login', data=dict(
            email='',
            password=''
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data, "Empty username and password should show error message")

class TestAdminAdd(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application context before each test method is run
        self.app = app.test_client()  # Create a test client for making requests
        self.context = app.app_context()
        self.context.push()
        app.config['TESTING'] = True  # Set testing mode to True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing

    def tearDown(self):
        # Pop the Flask application context after each test method is run
        self.context.pop()

    def test_valid_add_brand(self):
 
        # Send a POST request to add the product to the cart
        response = self.app.post('/addbrand', data=dict(
            brand='Marca Test'
        ), follow_redirects=True)

        # Check if the response contains the expected HTML content
        self.assertIn(b'was added to your database', response.data, "Adding a brand should give success message")

    def test_valid_add_category(self):

        # Send a POST request to add the product to the cart
        response = self.app.post('/addcat', data=dict(
            category='Category Test'
        ), follow_redirects=True)

        # Check if the response contains the expected HTML content
        self.assertIn(b'was added to your database', response.data, "Adding a category should give success message")
    

if __name__ == "__main__":
    unittest.main()
