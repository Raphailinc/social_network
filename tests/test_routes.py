import unittest
from manage import create_app
from app.models import db
from app.models import User, Post, Comment
from flask import url_for

from config import Config

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_registration_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_view_post_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='Test Content', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 302)

    def test_create_post_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.get('/create_post')
        self.assertEqual(response.status_code, 302)

    def test_edit_post_route(self):
        with self.app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', content='Test Content', user_id=user.id)
            db.session.add(post)
            db.session.commit()

            with self.client.session_transaction() as session:
                session['user_id'] = user.id

            response = self.client.get(url_for('app.edit_post', post_id=post.id))
            self.assertEqual(response.status_code, 302)

    def test_all_posts_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='Test Content', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.get('/all_posts')
        self.assertEqual(response.status_code, 200)

    def test_delete_post_route(self):
        with self.app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', content='Test Content', user_id=user.id)
            db.session.add(post)
            db.session.commit()

            with self.client.session_transaction() as session:
                session['user_id'] = user.id

            response = self.client.post(url_for('app.delete_post', post_id=post.id), follow_redirects=False)
            self.assertEqual(response.status_code, 302)

    def test_profile_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)

    def test_update_profile_image_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.post('/update_profile_image', data=dict(profile_image='test_image.jpg'),
                                    content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)

    def test_edit_comment_route(self):
        with self.app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', content='Test Content', user_id=user.id)
            db.session.add(post)
            db.session.commit()
            comment = Comment(content='Test Comment', post_id=post.id, user_id=user.id)
            db.session.add(comment)
            db.session.commit()

            with self.client.session_transaction() as session:
                session['user_id'] = user.id

            response = self.client.get(url_for('app.edit_comment', comment_id=comment.id))
            self.assertEqual(response.status_code, 302)

    def test_delete_comment_route(self):
        with self.app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', content='Test Content', user_id=user.id)
            db.session.add(post)
            db.session.commit()
            comment = Comment(content='Test Comment', post_id=post.id, user_id=user.id)
            db.session.add(comment)
            db.session.commit()

            with self.client.session_transaction() as session:
                session['user_id'] = user.id

            response = self.client.post(url_for('app.delete_comment', comment_id=comment.id), follow_redirects=False)
            self.assertEqual(response.status_code, 302)

    def test_logout_route(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        response = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()