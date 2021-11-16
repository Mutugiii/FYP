from django.test import TestCase
from django.contrib.auth import get_user_model

from api.serializers import UserRegisterSerializer, UserModelSerializer, ObtainTokenPairSerializer, PostSerializer

from api.models import Post
User = get_user_model()

class UserRegisterSerializerTest(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='Test', last_name='User', email='test@test.com', password='test2020', bio='Just a test user', location='Nairobi')
        self.user.save()
        self.serializer = UserRegisterSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        
        self.assertCountEqual(data.keys(), ['username', 'first_name', 'last_name', 'email', 'password', 'bio', 'location'])

    def test_field_contents(self):
        data = self.serializer.data
        
        self.assertEqual(data['username'], 'test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['email'], 'test@test.com')
        self.assertEqual(data['location'], 'Nairobi')

    def tearDown(self):
        User.objects.all().delete()

class UserModelSerializerTest(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='Test', last_name='User', email='test@test.com', password='test2020', bio='Just a test user', location='Nairobi')
        self.user.save()
        self.serializer = UserModelSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'bio', 'location'])

    def test_field_contents(self):
        data = self.serializer.data

        self.assertEqual(data['username'], 'test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['email'], 'test@test.com')
        self.assertEqual(data['location'], 'Nairobi')

    def tearDown(self):
        User.objects.all().delete()

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='Test', last_name='User', email='test@test.com', password='test2020', bio='Just a test user', location='Nairobi')
        self.user.save()
        self.post = Post(title='Hello World', about='Testing', user=self.user)
        self.post.save()

        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['id', 'title', 'about', 'user', 'posted'])
        
    def test_field_contents(self):
        data = self.serializer.data

        self.assertEqual(data['id'], self.post.pk)
        self.assertEqual(data['title'], 'Hello World')
        self.assertEqual(data['about'], 'Testing')
        self.assertEqual(data['user'], self.user.pk)
        
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()