from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Tests for Blogly"""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        test_user = User(first_name="Test", last_name="User", image_url="https://cdn-fastly.petguide.com/media/2022/02/16/8257228/maltipoo.jpg?size=720x845&nocrop=1")
        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id
        self.test_user = test_user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Tests if server responds with list containing test_user"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        """Tests if user profile is created and displayed"""
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
            self.assertIn(self.test_user.image_url[20], html)
   
    def test_add_user(self):
        """Tests if a new user is added to the page"""
        with app.test_client() as client:
            data = {"first-name": "Using", "last-name": "Test", "image-url": "https://www.spongebobshop.com/cdn/shop/products/SB-Standees-Spong-3_800x.jpg?v=1603744568"}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Using Test</a>", html)
    
       
    def test_delete_user(self):
        """Tests if a user is deleted"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.test_user.full_name, html)

            