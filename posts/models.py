""" Импорт моделей Джанго и функции get_user_model """
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    """ объявляем класс постов в блоге """
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, blank=True, null=True, related_name="group")
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.text, self.author.username)


class Group(models.Model):
    """ объявляем класс сообществ в блоге """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_author")
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
