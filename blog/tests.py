from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse

# Create your tests here.


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.post = Post.objects.create(
            title="This is a test post?",
            body="this is the content of the post",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "This is a test post?")
        self.assertEqual(self.post.body, "this is the content of the post")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "This is a test post?")
        self.assertEqual(self.post.get_absolute_url(), "/post/1")

    def test_home_url_is_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_url_is_ok(self):
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "the")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detail(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/123kfkdf")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "a")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_create_post(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "new post",
                "body": "this is the body for the new post",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "new post")
        self.assertEqual(Post.objects.last().body, "this is the body for the new post")

    def test_update_post(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {"title": "updated title", "body": "the updated body is here"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "updated title")
        self.assertEqual(Post.objects.last().body, "the updated body is here")

    def test_delete_post(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)
