from django.test import TestCase
from django.contrib.auth import get_user_model

from api.models import Post
User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='Test', last_name='User', email='test@test.com', password='test2020', bio='Just a test user', location='Nairobi')
        self.user.save()

    def test_isinstance(self):
        self.assertIsInstance(self.user, User)

    def test_save_user(self):
        self.all_users = User.objects.all()

        self.assertIn(self.user, self.all_users)
        self.assertTrue(len(self.all_users) == 1)
        self.assertTrue(User.objects.filter(
            username = self.user.username
        ).exists())

    def tearDown(self):
        User.objects.all().delete()

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='Test', last_name='User', email='test@test.com', password='test2020', bio='Just a test user', location='Nairobi')
        self.user.save()
        self.post = Post(title='Hello World', about='Testing', user=self.user)
        self.post.save()

        self.all_posts = Post.objects.all()
    
    def test_isinstance(self):
        self.assertIsInstance(self.post, Post)

    def test_save_post(self):
        self.assertIn(self.post, self.all_posts)
        self.assertTrue(len(self.all_posts) == 1)

    def test_update_post(self):
        self.post.about = "Updated Testing"
        self.assertEqual(self.post.about, "Updated Testing")

    def test_delete_post(self):
        self.post.delete()
        self.assertTrue(len(self.all_posts) == 0)
        
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()