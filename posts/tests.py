from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from .models import User, Post, Group, Follow

# Create your tests here.

class TestStringMethods(TestCase):
        def setUp(self):
                cache.clear()
                self.client = Client()
                self.user = User.objects.create_user(username="den", email="smth@smb.com", password="1337228Dio")
                self.author = User.objects.create_user(username="farthur", email="smb@smth.com", password="102938Far")

        def test_Profile(self):
                resp = self.client.get(reverse("profile", kwargs={"username" : self.user.username}))
                self.assertEqual(resp.status_code, 200)

        def test_New_post_auth(self):
                resp = self.client.get("/new/", follow=True)
                self.assertRedirects(resp, "/auth/login/?next=/new/", status_code=302, target_status_code=200)
                self.client.login(username="den", password="1337228Dio")
                resp = self.client.get("/new/", follow=True)
                self.assertEqual(resp.status_code, 200)

        def test_Post_check(self):
                self.client.login(username="den", password="1337228Dio")
                post_created = Post.objects.create(text="Some text", author=self.user)
                resp1 = self.client.get("")
                self.assertContains(resp1, "Some text")
                resp2 = self.client.get(reverse("profile", kwargs={"username" : self.user.username}))
                self.assertContains(resp2, "Some text")
                resp3 = self.client.get(reverse("post", kwargs={"username" : self.user.username, "post_id" : post_created.id}))
                self.assertContains(resp3, "Some text")
        
        def test_Edit_check(self):
                self.client.login(username="den", password="1337228Dio")
                post_created = Post.objects.create(text="Some text", author=self.user)
                self.client.post(reverse("post_edit", kwargs={"username" : self.user.username, "post_id" : post_created.id}), {"text" : "New Text"}, folloe=True)
                resp1 = self.client.get("")
                self.assertContains(resp1, "New Text")
                resp2 = self.client.get(reverse("profile", kwargs={"username" : self.user.username}))
                self.assertContains(resp2, "New Text")
                resp3 = self.client.get(reverse("post", kwargs={"username" : self.user.username, "post_id" : post_created.id}))
                self.assertContains(resp3, "New Text")

        def test_error_404(self):
                resp = self.client.get("/404/", follow=True)
                self.assertEqual(resp.status_code, 404)

        def test_image_check(self):
                self.client.login(username="den", password="1337228Dio")
                self.group = Group.objects.create(title="group", slug="test", description="some text")
                with open("media/posts/lr.jpg", "rb") as fp:
                        self.client.post("/new/", {"text" : "Some text", "image" : fp, "group" : self.group.id}, follow=True)
                        resp1 = self.client.get(reverse("index"))
                        self.assertContains(resp1, "<img")
                        resp2 = self.client.get(reverse("profile", kwargs={"username" : self.user.username}))
                        self.assertContains(resp2, "<img")
                        author = get_object_or_404(User, username="den")
                        post = Post.objects.get(author=author, text="Some text")
                        resp3 = self.client.get(reverse("post", kwargs={"username" : self.user.username, "post_id" : post.id}))
                        self.assertContains(resp3, "<img")
                        resp4 = self.client.get(reverse("group_posts", kwargs={"slug" : "test"}))
                        self.assertContains(resp4, "<img")
        
        def test_nonimage(self):
                self.client.login(username="den", password="1337228Dio")
                with open("C:/Dev/requirements.txt") as fp:
                        resp = self.client.post("/new/", {"text" : "Some text", "image" : fp}, follow=True)
                        self.assertNotContains(resp, "<img")

        def test_cache(self):
                self.client.login(username="den", password="1337228Dio")
                self.client.post("/new/", {"text" : "cache"})
                self.client.get("/")
                key = make_template_fragment_key("index_page")
                html_cache = cache.get(key)
                self.assertTrue(html_cache)
        
        def test_subscription(self):
                self.client.login(username="farthur", password="102938Far")
                self.client.post("/new/", {"text" : "follow me!"})
                self.client.logout()
                self.client.login(username="den", password="1337228Dio")
                self.client.get(reverse("profile_follow", kwargs={"username" : self.author.username}), follow=True)
                resp = self.client.get(reverse("follow_index"))
                self.assertContains(resp, "follow me!")
                self.client.get(reverse("profile_unfollow", kwargs={"username" : self.author.username}), follow=True)
                resp1 = self.client.get(reverse("follow_index"))
                self.assertNotContains(resp1, "follow me!")

        def test_follow_index(self):
                self.client.login(username="farthur", password="102938Far")
                self.client.post("/new/", {"text" : "follow me!"})
                resp = self.client.get(reverse("follow_index"))
                self.assertNotContains(resp, "follow me!")
                self.client.logout()
                self.client.login(username="den", password="1337228Dio")
                self.client.get(reverse("profile_follow", kwargs={"username" : self.author.username}), follow=True)
                resp1 = self.client.get(reverse("follow_index"))
                self.assertContains(resp1, "follow me!")

        def test_comments(self):
                self.client.login(username="farthur", password="102938Far")
                self.client.post("/new/", {"text" : "follow me!"})
                post = Post.objects.get(text="follow me!", author=self.author)
                resp = self.client.get(reverse("add_comment", kwargs={"username" : self.author.username, "post_id" : post.id}))
                self.assertEquals(resp.status_code, 200)
                self.client.logout()
                resp1 = self.client.get(reverse("add_comment", kwargs={"username" : self.author.username, "post_id" : post.id}))
                self.assertEquals(resp1.status_code, 302)
                